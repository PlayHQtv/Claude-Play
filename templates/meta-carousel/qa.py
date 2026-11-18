import warnings; warnings.filterwarnings('ignore', category=DeprecationWarning)
"""Pre-publish QA for rendered carousels. Run right after a renderer (it re-opens the _build/<slide>.html files).
Usage: python3 qa.py <out_dir>   -> prints a report, writes <out_dir>/_qa/sheet.jpg (TikTok UI zones drawn), exit 1 on errors.
Checks: fonts + images loaded, text outside the safe margin or under TikTok UI, clipped/overflowing text,
an OCR read-back of every slide (Tesseract) against the text that was rendered,
a legibility check (WCAG contrast of every text element against what is really behind it) and a spell check
(English, game terms in qa_words.txt)."""
import os, sys, glob, re, difflib
import render as R
from tiktok_overlay import ZONES

JS = r"""() => {
 const out = {fonts: [...document.fonts].filter(f => f.status === 'error').map(f => f.family), imgs: [], text: [], issues: []};
 for (const im of document.images) if (!im.complete || !im.naturalWidth) out.imgs.push(im.getAttribute('src'));
 const bgs = new Set(); for (const e of document.querySelectorAll('*')) { const m = getComputedStyle(e).backgroundImage.match(/url\("?([^")]+)"?\)/); if (m) bgs.add(m[1]); }
 out.bgs = [...bgs];
 const frame = e => e.closest('.top,.logo,.corner,.topo,.bg,.vign,.streak');
 for (const e of document.querySelectorAll('body *')) {
  if (frame(e)) continue;
  const own = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
  if (!own) continue;
  const rg = document.createRange(); const tops = new Set(); let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  for (const n of e.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { rg.selectNodeContents(n); for (const q of rg.getClientRects()) { tops.add(Math.round(q.top)); x0=Math.min(x0,q.left); y0=Math.min(y0,q.top); x1=Math.max(x1,q.right); y1=Math.max(y1,q.bottom); } }
  if (x1 < 0) continue;
  const fr = (() => { const r2 = document.createRange(); r2.selectNodeContents(e); return r2.getBoundingClientRect(); })();
  out.text.push({t: own, full: e.innerText || own, fx0: fr.left, fy0: fr.top, fx1: fr.right, fy1: fr.bottom, lines: tops.size, x0, y0, x1, y1, gr: !!e.closest('.gr'), glow: !!e.closest('.neon'), hidden: getComputedStyle(e).visibility === 'hidden'});
  if (e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== 'visible') out.issues.push('clipped text: ' + own.slice(0, 40));
 }
 return out;
}"""


def _lum(px):
    import numpy as np
    c = px / 255.0; c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def legib(nm, texts, withtext, notext, warns):
    """Text pixels = pixels that change when the glyphs are hidden. Contrast = WCAG ratio between the text pixels and
    the background right behind them (same pixels in the text-less render). < 3:1 is hard to read on a phone."""
    import numpy as np
    A, B = np.asarray(withtext, np.float32), np.asarray(notext, np.float32)
    for t in texts:
        x0, y0, x1, y1 = max(0, int(t['x0'])), max(0, int(t['y0'])), min(1080, int(t['x1'])), min(1440, int(t['y1']))
        if x1 - x0 < 10 or y1 - y0 < 8 or len(re.sub(r'\W', '', t['t'])) < 3 or t.get('glow'): continue
        a, b = A[y0:y1, x0:x1], B[y0:y1, x0:x1]
        m = np.abs(a - b).sum(-1) > 60
        if m.sum() < 30: continue
        lt, lb = np.median(_lum(a[m])), np.median(_lum(b[m]))
        r = (max(lt, lb) + 0.05) / (min(lt, lb) + 0.05)
        if r < 3: warns.append(f'{nm}: low contrast {r:.1f}:1 for "{t["t"][:40]}" - darken/lighten what is behind it')


def faces(nm, texts, notext, warns):
    """Faces in the artwork (YuNet, detected on the render WITHOUT text) must not be covered by text."""
    mp = os.path.join(os.environ.get('PHQ_MODELS', '/tmp/models'), 'yunet.onnx')
    if not os.path.exists(mp): warns.append('face check skipped (bin/models.sh)'); return
    import cv2, numpy as np
    im = cv2.cvtColor(np.asarray(notext), cv2.COLOR_RGB2BGR)
    det = cv2.FaceDetectorYN.create(mp, '', (im.shape[1], im.shape[0]), 0.7)
    _, fs = det.detect(im)
    for fx, fy, fw, fh in ([] if fs is None else [x[:4] for x in fs]):
        if fw < 40: continue  # tiny background people
        for t in texts:
            ix = min(t['x1'], fx + fw) - max(t['x0'], fx); iy = min(t['y1'], fy + fh) - max(t['y0'], fy)
            if ix > 0 and iy > 0 and ix * iy > 0.12 * fw * fh:
                warns.append(f'{nm}: text covers a face ({int(fx)},{int(fy)}): "{t["t"][:40]}" - move the text or the image'); break


def spell(texts, warns, nm):
    try:
        from spellchecker import SpellChecker
    except ImportError:
        warns.append('spell check skipped (pip install pyspellchecker)'); return
    sc = SpellChecker()
    wl = os.path.join(R.HERE, 'qa_words.txt')
    if os.path.exists(wl): sc.word_frequency.load_words([w.strip().lower() for w in open(wl) if w.strip() and not w.startswith('#')])
    words = set()
    for t in texts:
        for w in re.findall(r"[A-Za-z][A-Za-z']+", t['t']):
            w = w.strip("'").lower()
            if len(w) >= 3 and not w.endswith("'s"): words.add(w)
    bad = sorted(sc.unknown(words))
    if bad: warns.append(f'{nm}: unknown words (typo?) {", ".join(bad[:12])} - fix or add to qa_words.txt')


def check(out_dir):
    import pytesseract
    from PIL import Image, ImageDraw
    from playwright.sync_api import sync_playwright
    slides = sorted(glob.glob(os.path.join(out_dir, '*.jpg')))
    errs, warns, sheet, jobs = [], [], [], []
    srv = R.serve(R.HERE); port = srv.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}); pg3 = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=3)
        for f in slides:
            nm = os.path.splitext(os.path.basename(f))[0]
            html = os.path.join(R.HERE, '_build', nm + '.html')
            if not os.path.exists(html):
                warns.append(f'{nm}: no html, DOM checks skipped'); continue
            pg.goto(f'http://127.0.0.1:{port}/_build/{nm}.html'); pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(300)
            d = pg.evaluate(JS)
            for u in d['bgs']:
                if u.startswith('/') and not os.path.exists(os.path.join(R.HERE, u.lstrip('/'))): errs.append(f'{nm}: missing image {u}')
            errs += [f'{nm}: font not loaded {x}' for x in d['fonts']] + [f'{nm}: image not loaded {x}' for x in d['imgs']]
            errs += [f'{nm}: {x}' for x in d['issues']]
            spell(d['text'], warns, nm)
            for t in d['text']:
                if t['x0'] < 40 or t['x1'] > 1040 or t['y1'] > 1420:
                    errs.append(f'{nm}: outside safe margin: "{t["t"][:40]}"')
                for z in ZONES:
                    if t['x0'] < z[2] and t['x1'] > z[0] and t['y0'] < z[3] and t['y1'] > z[1]:
                        warns.append(f'{nm}: under TikTok UI {z}: "{t["t"][:40]}"'); break
            # grunge legibility: the grunge mask must not cut a letter horizontally (the old 'NIGHTSHADE -> NiGHTSHADE' bug)
            import io
            from PIL import Image as _I
            chars = pg.evaluate("""() => [...document.querySelectorAll('.gr')].map((e, k) => { e.dataset.qa = k; const rg = document.createRange(); const out = [];
              const tn = [...e.childNodes].find(n => n.nodeType === 3); if (!tn) return null;
              for (let i = 0; i < tn.length; i++) { const ch = tn.textContent[i]; if (!ch.trim()) continue; rg.setStart(tn, i); rg.setEnd(tn, i + 1); const r = rg.getBoundingClientRect(); out.push([ch, r.left, r.top, r.width, r.height]); }
              return out; })""")
            pg3.goto(f'http://127.0.0.1:{port}/_build/{nm}.html'); pg3.wait_for_selector('body[data-ready]'); pg3.wait_for_timeout(300)
            shot = lambda: _I.open(io.BytesIO(pg3.screenshot())).convert('L')
            rgb3 = _I.open(io.BytesIO(pg3.screenshot())).convert('RGB')  # 3x render WITH text (for the glyph-mask OCR)
            a = rgb3.convert('L'); pg3.add_style_tag(content='.gr{-webkit-mask-image:none!important}'); pg3.wait_for_timeout(100); bimg = shot()
            # legibility: same page with every glyph invisible -> what is really behind the text
            pg3.add_style_tag(content='body *:not(.idx){color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}.h em,.big,.fol em,.hdr b,.body .hl,.facts strong{background:none!important}')
            # gradient text (background-clip:text) keeps its gradient box when the glyphs go transparent -> drop it too
            pg3.evaluate("() => document.querySelectorAll('body *').forEach(e => { const cs = getComputedStyle(e); if ((cs.webkitBackgroundClip || cs.backgroundClip) === 'text') e.style.setProperty('background', 'none', 'important'); })")
            pg3.wait_for_timeout(150); notext3 = _I.open(io.BytesIO(pg3.screenshot())).convert('RGB'); notext = notext3.resize((1080, 1440))
            withtext = _I.open(f).convert('RGB')
            legib(nm, d['text'], withtext, notext, warns)
            faces(nm, d['text'], notext, warns)
            # OCR read-back, element by element (crop of the rendered slide -> Tesseract single-line mode)
            from PIL import ImageFilter, ImageOps
            # Glyph mask = pixels that change when the text is made invisible (3x render with text vs. without text).
            # That isolates the real rendered letters from photos, gradients and HUD textures, so Tesseract reads the
            # glyphs themselves (gradient/gold/grunge titles were false 'OCR reads ...' warnings before, user 17.11.2026).
            import numpy as _np
            # Clean glyph render: same page, every photo/texture/gradient/shadow/glow removed, all text pure black on white.
            # Fonts, sizes, line breaks, clipping and grunge masks stay exactly as rendered.
            pg3.add_style_tag(content='html body *:not(.zzqa){color:#000!important;-webkit-text-fill-color:#000!important;text-shadow:none!important;'
                              'background:none!important;box-shadow:none!important;filter:none!important;border-color:transparent!important;opacity:1!important}'
                              'html body{background:#fff!important}html body img,html body video,html body svg{visibility:hidden!important}'
                              'html body *::before,html body *::after{display:none!important}')
            pg3.wait_for_timeout(150)
            clean = _np.asarray(_I.open(io.BytesIO(pg3.screenshot())).convert('L'))
            # grunge cut check on the clean render (black glyphs on white): with mask vs. without mask. The gold gradient's
            # dark band made the old colour-based check report cuts that are not there (user 17.11.2026).
            pg3.add_style_tag(content='html body .gr{-webkit-mask-image:none!important}'); pg3.wait_for_timeout(100)
            clean_nomask = _I.open(io.BytesIO(pg3.screenshot())).convert('L')
            a = _I.fromarray(255 - clean); bimg = clean_nomask.point(lambda v: 255 - v)
            for grp in chars or []:
                for ch, x, y, w, h in grp or []:
                    box = (int(3 * x) + 3, int(3 * (y + h * 0.15)), int(3 * (x + w)) - 3, int(3 * (y + h * 0.88)))
                    if box[2] <= box[0] or box[3] <= box[1]: continue
                    A, B = a.crop(box), bimg.crop(box); W_ = A.width
                    pa, pb = list(A.getdata()), list(B.getdata())
                    run = best = 0
                    for yy in range(A.height):
                        rb = sum(1 for v in pb[yy * W_:(yy + 1) * W_] if v > 110); ra = sum(1 for v in pa[yy * W_:(yy + 1) * W_] if v > 110)
                        run = run + 1 if (rb >= 8 and ra / rb < 0.45) else 0; best = max(best, run)
                    gh = 0.67 * h  # glyph height (cap height) inside the line box
                    if best >= max(5, int(0.03 * 3 * gh)):
                        msg = f'{nm}: grunge mask cuts through letter "{ch}" ({best // 3}px gap) - shift mask_pos'
                        # thin letters (I, 1, J, L, T ...) can turn into another letter (I -> i): hard error; wide letters: check visually
                        (errs if w / gh < 0.4 else warns).append(msg)

            gm = clean < 128
            changed = _np.abs(_np.asarray(rgb3, _np.int16) - _np.asarray(notext3, _np.int16)).sum(-1) > 30
            glyph = Image.fromarray(_np.where(gm, 0, 255).astype(_np.uint8))
            for t in d['text']:
                # covered / invisible text: glyph pixels that do not change the real slide when the text is hidden
                bx = (max(0, int(t['x0'])) * 3, max(0, int(t['y0'])) * 3, min(1080, int(t['x1'])) * 3, min(1440, int(t['y1'])) * 3)
                g = gm[bx[1]:bx[3], bx[0]:bx[2]]
                if g.sum() > 200 and not t.get('hidden'):
                    cov = (g & changed[bx[1]:bx[3], bx[0]:bx[2]]).sum() / g.sum()
                    if cov < 0.3: warns.append(f'{nm}: text hidden or covered ({cov:.0%} visible): "{t["t"][:40]}"')
                want = re.sub(r'[^A-Z0-9]', '', t['t'].upper())
                if len(want) < 3 or (t['gr'] and len(want) < 4): continue
                full = (t.get('full') or t['t']).upper()
                want = re.sub(r'[^A-Z0-9]', '', full)  # the crop also shows inline children (<b>, <span>)
                if '%' in full: want += '|' + re.sub(r'[^A-Z0-9]', '', full.replace('%', '0'))  # Tesseract often reads % as O/0
                if os.environ.get('QA_DEBUG'): t['_dbg'] = True
                if t.get('glow'): continue  # neon script lettering: Tesseract cannot read script fonts; covered by the visibility check above
                if (t.get('full') or '').strip() != t['t'].strip() and t.get('fx1', 0) > 0:  # inline children: OCR the whole element box
                    lh = (t['y1'] - t['y0']) / max(1, t['lines'])
                    t = dict(t, x0=min(t['x0'], t['fx0']), y0=min(t['y0'], t['fy0']), x1=max(t['x1'], t['fx1']), y1=max(t['y1'], t['fy1']))
                    t['lines'] = max(t['lines'], round((t['y1'] - t['y0']) / max(1, lh)))
                box = (max(0, int(t['x0']) - 4) * 3, max(0, int(t['y0'])) * 3, min(1080, int(t['x1']) + 4) * 3, min(1440, int(t['y1'])) * 3)
                c = glyph.crop(box)
                if t['gr']: c = c.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(7))  # close the grunge holes (clean render has no other texture)
                if t['lines'] <= 1:  # line boxes overlap neighbours (kicker above, tagline below): keep only the tallest ink band
                    ink = (_np.asarray(c) < 128).sum(1) > max(2, c.width // 200)
                    best, cur, st = (0, 0, c.height), 0, 0
                    for yy, on in enumerate(list(ink) + [False]):
                        if on: cur += 1
                        else:
                            if cur > best[0]: best = (cur, yy - cur, yy)
                            cur = 0
                    if best[0] > 10: c = c.crop((0, max(0, best[1] - 6), c.width, min(c.height, best[2] + 6)))
                h = c.height // max(1, t['lines'])
                if h > 150: c = c.resize((max(1, c.width * 120 // h), max(1, c.height * 120 // h)), Image.LANCZOS)  # Tesseract likes ~100 px glyphs
                c = ImageOps.expand(c, 40, fill=255)
                if t.get('_dbg'): os.makedirs('/tmp/qa_dbg', exist_ok=True); c.save(f'/tmp/qa_dbg/{nm}_{want.split("|")[0][:14]}.png')
                jobs.append((nm, want, c, '--psm 7' if t['lines'] <= 1 else '--psm 6'))
            ov = Image.open(f).convert('RGBA'); lay = Image.new('RGBA', ov.size); dr = ImageDraw.Draw(lay)
            for z in ZONES: dr.rectangle(z, fill=(255, 0, 60, 70), outline=(255, 0, 60, 255), width=3)
            sheet.append(Image.alpha_composite(ov, lay).convert('RGB'))
        b.close()
    srv.shutdown()
    # OCR in parallel (Tesseract runs as separate processes)
    from concurrent.futures import ThreadPoolExecutor
    # Cut-outs must be complete figures (user 18.11.2026: badly cut Jason & Lucia photo on the release-time cover).
    # A cut-out whose TOP edge is opaque was cropped from a frame (head/hair cut flat) -> real warning.
    import glob as _g, numpy as _n
    seen = set()
    for hp in sorted(_g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_build', '*.html'))):
        for m in re.finditer(r'(_build/(?:gta|s1|w)/(cut_[\w-]+\.png))', open(hp, encoding='utf-8').read()):
            fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), m.group(1))
            if fp in seen or not os.path.exists(fp): continue
            seen.add(fp)
            al = _n.asarray(Image.open(fp).convert('RGBA'))[:, :, 3] > 200
            # user 18.11.2026: "Dieser Fehler darf nie passieren" -> hard ERROR (exit 1, post must not go out)
            tint = _n.asarray(Image.open(fp).convert('RGB'), float)[al]
            mono = tint.size and (tint[:, 2].mean() - tint[:, 1].mean()) > 45  # strong purple/blue colour cast = photo crop, not artwork
            if al[0].mean() > 0.03:
                errs.append(f'cut-out {m.group(2)} is CROPPED ({al[0].mean():.0%} of the top edge opaque) - head/figure cut off. Use a complete official artwork cut-out')
            if mono:
                errs.append(f'cut-out {m.group(2)} has a strong colour cast (screenshot/photo crop) - use a clean official artwork cut-out')
    from PIL import ImageFilter as _F, ImageOps as _O
    def score(want, got):
        got = got.replace('O', '0').replace('I', '1').replace('S', '5'); w2 = want.replace('O', '0').replace('I', '1').replace('S', '5')
        r = difflib.SequenceMatcher(None, w2, got).ratio()
        if len(got) > len(w2):  # crop may include neighbours: best matching window
            r = max([r] + [difflib.SequenceMatcher(None, w2, got[i:i + len(w2)]).ratio() for i in range(len(got) - len(w2) + 1)])
        return r
    def run(j):
        # Tesseract struggles with very heavy condensed display fonts (Anton): try a few clean variants of the SAME glyph
        # mask (as is, slightly thinned, thinned + ~80 px) and two page modes; the text passes if any reading matches.
        nm, want, c, cfg = j
        def thin(k, h=None, sx=1.0):
            v = c.filter(_F.MaxFilter(k)) if k else c
            if h and v.height > h: v = v.resize((max(1, v.width * h // v.height), h))
            if sx != 1.0: v = v.resize((int(v.width * sx), v.height))  # un-condense very narrow display fonts
            return _O.expand(v, 30, fill=255)
        variants = [(c, cfg)] + ([(c, '--psm 8'), (thin(5), '--psm 7'), (thin(5), '--psm 8'), (thin(7, 80), '--psm 7'),
                                  (thin(0, sx=1.5), '--psm 7'), (thin(3, sx=1.6), '--psm 7'), (thin(0, sx=2.0), '--psm 7')]
                                 if cfg == '--psm 7' else [(thin(3), cfg), (thin(0, sx=1.5), cfg)])
        best = (-1, '')
        for img, cf in variants:
            got = re.sub(r'[^A-Z0-9]', '', pytesseract.image_to_string(img, config=cf).upper())
            r = max(score(w, got) for w in want.split('|'))
            if r > best[0]: best = (r, got)
            if r >= 0.8: break
        return nm, want, best
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 2) * 2)) as ex:
        for nm, want, (r, got) in ex.map(run, jobs):
            if r < 0.8: warns.append(f'{nm}: OCR reads "{got[:30]}" for "{want.split("|")[0][:30]}" ({r:.2f}) - check visually')
    q = os.path.join(out_dir, '_qa'); os.makedirs(q, exist_ok=True)
    if sheet:
        S = Image.new('RGB', (360 * len(sheet), 480))
        for i, s in enumerate(sheet): S.paste(s.resize((360, 480)), (i * 360, 0))
        S.save(os.path.join(q, 'sheet.jpg'), quality=88)
    print(f'QA {out_dir}: {len(slides)} slides, {len(errs)} errors, {len(warns)} warnings')
    for e in errs: print('  ERROR', e)
    for w in warns: print('  warn ', w)
    return not errs


if __name__ == '__main__':
    if sys.argv[1] == '--caption':  # spell check a TikTok caption / title / first comment: qa.py --caption "text"
        w = []; spell([{'t': re.sub(r'[#@]\w+', '', ' '.join(sys.argv[2:]))}], w, 'caption'); print('\n'.join(w) or 'caption OK'); sys.exit(1 if w else 0)
    sys.exit(0 if check(sys.argv[1]) else 1)
