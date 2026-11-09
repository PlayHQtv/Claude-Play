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
  out.text.push({t: own, lines: tops.size, x0, y0, x1, y1, gr: !!e.closest('.gr'), glow: !!e.closest('.neon'), hidden: getComputedStyle(e).visibility === 'hidden'});
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
            a = shot(); pg3.add_style_tag(content='.gr{-webkit-mask-image:none!important}'); pg3.wait_for_timeout(100); bimg = shot()
            # legibility: same page with every glyph invisible -> what is really behind the text
            pg3.add_style_tag(content='body *:not(.idx){color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}.h em,.big,.fol em,.hdr b,.body .hl,.facts strong{background:none!important}')
            pg3.wait_for_timeout(150); notext = _I.open(io.BytesIO(pg3.screenshot())).convert('RGB').resize((1080, 1440))
            withtext = _I.open(f).convert('RGB')
            legib(nm, d['text'], withtext, notext, warns)
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
            # OCR read-back, element by element (crop of the rendered slide -> Tesseract single-line mode)
            from PIL import ImageFilter, ImageOps
            src = Image.open(f).convert('L')
            for t in d['text']:
                want = re.sub(r'[^A-Z0-9]', '', t['t'].upper())
                if len(want) < 3 or (t['gr'] and len(want) < 4): continue
                box = (max(0, int(t['x0']) - 4), max(0, int(t['y0'])), min(1080, int(t['x1']) + 4), min(1440, int(t['y1'])))
                c = src.crop(box); c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
                if t['gr']: c = c.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
                if c.resize((1, 1)).getpixel((0, 0)) < 128: c = c.point(lambda v: 255 - v)  # dark text on light for Tesseract
                import numpy as _np
                arr = _np.asarray(c); hist = _np.bincount(arr.ravel(), minlength=256).astype(float); tot = arr.size
                cs, mu = _np.cumsum(hist), _np.cumsum(hist * _np.arange(256))
                with _np.errstate(divide='ignore', invalid='ignore'):
                    var = (mu[-1] * cs / tot - mu) ** 2 / (cs * (tot - cs))
                th = int(_np.nanargmax(var))  # Otsu threshold
                c = ImageOps.expand(c.point(lambda v, th=th: 0 if v <= th else 255), 30, fill=255)
                jobs.append((nm, want, c, '--psm 7' if t['lines'] <= 1 else '--psm 6'))
            ov = Image.open(f).convert('RGBA'); lay = Image.new('RGBA', ov.size); dr = ImageDraw.Draw(lay)
            for z in ZONES: dr.rectangle(z, fill=(255, 0, 60, 70), outline=(255, 0, 60, 255), width=3)
            sheet.append(Image.alpha_composite(ov, lay).convert('RGB'))
        b.close()
    srv.shutdown()
    # OCR in parallel (Tesseract runs as separate processes)
    from concurrent.futures import ThreadPoolExecutor
    def run(j):
        nm, want, c, cfg = j
        return nm, want, re.sub(r'[^A-Z0-9]', '', pytesseract.image_to_string(c, config=cfg).upper())
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 2) * 2)) as ex:
        for nm, want, got in ex.map(run, jobs):
            got = got.replace('O', '0').replace('I', '1').replace('S', '5'); w2 = want.replace('O', '0').replace('I', '1').replace('S', '5')
            r = difflib.SequenceMatcher(None, w2, got).ratio()
            if len(got) > len(w2):  # crop may include neighbours: best matching window
                r = max([r] + [difflib.SequenceMatcher(None, w2, got[i:i + len(w2)]).ratio() for i in range(len(got) - len(w2) + 1)])
            if r < 0.8: warns.append(f'{nm}: OCR reads "{got[:30]}" for "{want[:30]}" ({r:.2f}) - check visually')
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
