"""PlayHQ GTA VI carousel v3 – editorial / premium.
One tip per slide: official 4K screenshot (uncropped, full width) on an ambient extension of itself, huge outlined
index number, display title, short body, source line. Cover: box-art collage + official character art + neon title.
Usage: python3 gta3_render.py data/<file>.json <out_dir>. Private images live in _build/gta/."""
import json, os, sys
import render as R

E = R.E
CSS = """
@font-face{font-family:BS;src:url(/assets/fonts/BigShoulders-900.woff2);font-weight:900}
@font-face{font-family:BS;src:url(/assets/fonts/BigShoulders-800.woff2);font-weight:800}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-500.woff2);font-weight:500}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-600.woff2);font-weight:600}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-700.woff2);font-weight:700}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-800.woff2);font-weight:800}
@font-face{font-family:Tail;src:url(/assets/fonts/Yellowtail.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
:root{--p:#ff3d9a;--o:#ff9f43;--y:#ffd36b;--v:#7b3cff;--t:#2fe3d0;--ink:#0c0512}
html,body{width:1080px;height:1440px;overflow:hidden}
body{position:relative;background:var(--ink);color:#fff;font-family:IT;-webkit-font-smoothing:antialiased}
.amb{position:absolute;inset:0;background-size:cover;background-position:center}
.tint{position:absolute;inset:0;background:
 radial-gradient(900px 520px at 100% 0%,rgba(255,61,154,.38),transparent 70%),
 radial-gradient(800px 600px at 0% 100%,rgba(123,60,255,.35),transparent 70%),
 linear-gradient(180deg,rgba(12,5,18,.25) 0%,rgba(12,5,18,.15) 40%,rgba(12,5,18,.88) 78%,rgba(12,5,18,.97) 100%)}
.grain{position:absolute;inset:0;background:url(/assets/grain.png);mix-blend-mode:overlay;opacity:.13;pointer-events:none}
.leak{position:absolute;width:900px;height:900px;border-radius:50%;filter:blur(90px);opacity:.35;mix-blend-mode:screen}
.hdr{position:absolute;left:60px;top:126px;display:flex;align-items:center;gap:14px}
.hdr i{display:block;width:44px;height:4px;background:linear-gradient(90deg,var(--o),var(--p))}
.hdr span{font-family:IT;font-weight:800;font-size:24px;letter-spacing:6px;color:#fff}
.hdr b{font-family:IT;font-weight:800;font-size:24px;letter-spacing:6px;background:linear-gradient(90deg,#ffb15c,#ff4f8b);-webkit-background-clip:text;color:transparent}
.plogo{position:absolute;right:170px;top:104px;width:84px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}
.glogo{position:absolute;left:56px;top:104px;height:150px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.65))}
.shot{position:absolute;left:0;width:1080px;background-size:100% 100%;
 -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 9%,#000 82%,transparent 100%)}
.shot::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,5,18,.0) 55%,rgba(12,5,18,.55) 100%)}
.idx{position:absolute;left:44px;font-family:BS;font-weight:900;line-height:.8;letter-spacing:-6px;color:transparent;
 -webkit-text-stroke:3px rgba(255,255,255,.92);text-shadow:0 0 40px rgba(255,61,154,.55)}
.idx.fill{background:linear-gradient(180deg,#ffd27a 0%,#ff8a4c 35%,#ff4f8b 65%,#d63ac7 100%);-webkit-background-clip:text;-webkit-text-stroke:0;
 filter:drop-shadow(-3px 0 0 rgba(255,0,90,.45)) drop-shadow(3px 0 0 rgba(0,220,255,.35)) drop-shadow(0 12px 34px rgba(255,61,154,.5))}
.k{position:absolute;left:62px;font-family:IT;font-weight:800;font-size:24px;letter-spacing:7px;color:var(--t)}
.h{position:absolute;left:58px;font-family:BS;font-weight:900;line-height:.9;letter-spacing:.5px;white-space:nowrap;color:#fff;text-transform:uppercase;
 text-shadow:0 2px 0 rgba(0,0,0,.25),0 18px 40px rgba(0,0,0,.55)}
.h em{font-style:normal;background:linear-gradient(180deg,#ffd27a 8%,#ff8a4c 42%,#ff4f8b 70%,#d63ac7 100%);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 22px rgba(255,79,139,.45))}
.body{position:absolute;left:62px;width:880px;font-family:IT;font-weight:500;font-size:37px;line-height:1.32;color:rgba(255,240,248,.92)}
.body b{font-weight:800;color:#fff}
.body .hl{font-weight:800;background:linear-gradient(90deg,var(--y),var(--p));-webkit-background-clip:text;color:transparent}
.facts{position:absolute;left:62px;width:880px;display:flex;gap:44px}
.facts div{flex:1;border-top:3px solid;border-image:linear-gradient(90deg,var(--o),var(--p)) 1;padding-top:16px}
.facts small{display:block;font-family:IT;font-weight:800;font-size:22px;letter-spacing:5px;color:rgba(255,255,255,.65)}
.facts strong{display:block;font-family:BS;font-weight:900;font-size:66px;line-height:1;margin-top:8px;color:#fff}
.facts p{font-family:IT;font-weight:600;font-size:27px;line-height:1.3;color:rgba(255,240,248,.85);margin-top:8px}
.src{position:absolute;left:62px;bottom:104px;font-family:IT;font-weight:600;font-size:14px;letter-spacing:1.5px;color:rgba(255,255,255,.42)}
.src::before{content:"";display:inline-block;width:16px;height:2px;background:var(--p);vertical-align:middle;margin-right:12px}
.prog{position:absolute;right:170px;bottom:118px;display:flex;gap:8px}
.prog i{display:block;width:30px;height:5px;border-radius:3px;background:rgba(255,255,255,.25)}
.prog i.on{background:linear-gradient(90deg,var(--o),var(--p))}
.panel{position:absolute;background-size:100% 100%;outline:8px solid #fff;outline-offset:-1px;box-shadow:0 30px 60px rgba(0,0,0,.6)}
.panel span{position:absolute;left:18px;top:-24px;font-family:IT;font-weight:800;font-size:22px;letter-spacing:5px;background:#fff;color:var(--ink);padding:9px 14px 7px}
.fg{position:absolute;left:0;width:1080px;background-size:100% 100%}
.fg.m{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 9%,#000 82%,transparent 100%)}
.big{position:absolute;left:50%;transform:translateX(-50%);font-family:BS;font-weight:900;line-height:.82;white-space:nowrap;text-transform:uppercase;
 background:linear-gradient(180deg,#ffd27a 8%,#ff8a4c 42%,#ff4f8b 70%,#d63ac7 100%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(-4px 0 0 rgba(255,0,90,.4)) drop-shadow(4px 0 0 rgba(0,220,255,.3)) drop-shadow(0 20px 50px rgba(0,0,0,.45))}
.cut{position:absolute;filter:drop-shadow(0 40px 50px rgba(0,0,0,.65));-webkit-mask-image:linear-gradient(180deg,#000 82%,transparent 99%)}
.neon{position:absolute;left:66px;font-family:Tail;white-space:nowrap;color:#fff;transform:rotate(-5deg);
 text-shadow:0 0 4px #fff,0 0 12px var(--p),0 0 28px var(--p),0 0 60px rgba(255,61,154,.8)}
.sun{position:absolute;border-radius:50%;background:linear-gradient(180deg,var(--y) 0%,var(--o) 42%,var(--p) 78%,var(--v) 100%);
 -webkit-mask-image:linear-gradient(180deg,#000 0 48%,transparent 48%),repeating-linear-gradient(180deg,#000 0 22px,transparent 22px 34px);opacity:.9;
 filter:drop-shadow(0 0 80px rgba(255,61,154,.6))}
.swipe{position:absolute;left:62px;font-family:IT;font-weight:800;font-size:26px;letter-spacing:7px;color:#fff}
.swipe b{color:var(--p)}
.save{position:absolute;left:62px;padding:22px 30px 18px;background:linear-gradient(100deg,var(--y),var(--o) 35%,var(--p));color:var(--ink);transform:skewX(-8deg);box-shadow:0 20px 50px rgba(255,61,154,.45)}
.save small{display:block;font-family:IT;font-weight:800;font-size:22px;letter-spacing:6px}
.save strong{display:block;font-family:BS;font-weight:900;font-size:92px;line-height:.95}
.fol{position:absolute;left:62px;font-family:BS;font-weight:900;font-size:70px;line-height:1;color:#fff}
.fol em{font-style:normal;text-shadow:none;background:linear-gradient(90deg,#ffb15c,#ff4f8b);-webkit-background-clip:text;color:transparent}
"""


# Official Rockstar screenshot location of every graded image (verified 11.11. by keypoint match against the
# official file names, e.g. Port_Gellhorn_01). Used for the v4 location label; set "loc" in the data to override.
LOC = {'g_skyline': 'VICE CITY', 'g_keys': 'LEONIDA KEYS', 'g_motel': 'PORT GELLHORN', 'g_club': 'VICE CITY',
       'g_rooftop': 'VICE CITY', 'g_sign': 'VICE CITY', 'g_grass': 'GRASSRIVERS', 'g_kalaga': 'MOUNT KALAGA',
       'g_vc14': 'VICE CITY', 'g_vc15': 'VICE CITY', 'g_vc16': 'VICE CITY', 'g_vc17': 'VICE CITY', 'g_vc19': 'VICE CITY',
       'g_vc20': 'VICE CITY', 'g_gr07': 'GRASSRIVERS', 'g_lk07': 'LEONIDA KEYS', 'g_vc22': 'VICE CITY', 'g_vc24': 'VICE CITY', 'g_vc26': 'VICE CITY', 'g_vc27': 'VICE CITY', 'g_gr08': 'GRASSRIVERS',
       'g_uult02': 'ULTIMATE EDITION', 'g_ucheetah1': "'95 GROTTI CHEETAH", 'g_ucheetah2': "'95 GROTTI CHEETAH", 'g_ustanier': "'55 VAPID STANIER",
       'g_urevolvers': 'HAWK + LITTLE MORGAN', 'g_usafehouse': "JASON'S SAFEHOUSE", 'g_uvvc': 'VINTAGE VICE CITY PACK', 'g_ulooks': 'VINTAGE VICE CITY PACK'}  # official Rockstar file names (Launch Gallery)

V4CSS = '''
.hdr{left:44px;top:112px;padding:14px 26px 14px 20px;border-radius:40px;background:rgba(14,6,24,.55);backdrop-filter:blur(18px);
 border:1px solid rgba(255,255,255,.14);box-shadow:0 10px 40px rgba(0,0,0,.35)}
.hdr b{background:linear-gradient(90deg,#ffd27a,#ff8a4c 55%,#ff6aa8);-webkit-background-clip:text}
.card{position:absolute;left:30px;width:1020px;bottom:70px;border-radius:34px;background:linear-gradient(180deg,rgba(28,10,40,.62),rgba(12,5,22,.78));
 backdrop-filter:blur(26px) saturate(1.3);border:1px solid rgba(255,255,255,.13);box-shadow:0 30px 80px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.12)}
.card:before{content:'';position:absolute;left:34px;right:34px;top:-1px;height:3px;border-radius:3px;background:linear-gradient(90deg,transparent,#ffb15c 20%,#ff4f8b 60%,#b44cff 85%,transparent)}
.loc{position:absolute;left:44px;padding:10px 18px 10px 14px;border-radius:30px;background:rgba(10,4,18,.62);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.18);
 font-family:IT;font-weight:800;font-size:21px;letter-spacing:4px;color:#fff;display:flex;align-items:center;gap:10px}
.loc i{width:10px;height:10px;border-radius:50%;background:#ff4f8b;box-shadow:0 0 0 5px rgba(255,79,139,.25)}
.src{bottom:96px;left:72px}
.prog{bottom:100px;right:72px}
.idx{z-index:3}
'''


def base(body, d, amb=None, cover=False, idx=None, total=None):
    prog = ''
    if idx is not None and total:
        prog = '<div class="prog">' + ''.join(f'<i class="{"on" if i == idx else ""}"></i>' for i in range(total)) + '</div>'
    head = ('<img class="glogo" src="/_build/gta/logo_gta6.png">' if cover else
            f'<div class="hdr"><i></i><span>GTA 6</span><b>{E(d.get("hdr", "TIPS & TRICKS"))}</b></div>')
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + (V4CSS if d.get('style', 'v4') == 'v4' else '') + '</style></head><body>'
            + (f'<div class="amb" style="background-image:url(/_build/gta/{amb})"></div>' if amb else '')
            + '<div class="leak" style="right:-380px;top:-300px;background:#ff3d9a"></div><div class="leak" style="left:-420px;bottom:-380px;background:#7b3cff"></div>'
            + '<div class="tint"></div>' + body + head + '<img class="plogo" src="/assets/logo.png">' + prog
            + (f'<div class="src">{E(d["source"])}</div>' if d.get('source') and not cover else '')
            + '<div class="grain"></div>' + R.FITJS + '</body></html>')


def cover(d):
    c = d['cover']
    cut = c.get('cutout')
    panels = ''.join(f'<div class="panel" style="left:{p["x"]}px;top:{p["y"]}px;width:{p["w"]}px;height:{round(p["w"] * 9 / 16)}px;transform:rotate({p.get("r", 0)}deg);background-image:url(/_build/gta/{p["img"]})">'
                     + (f'<span>{E(p["label"])}</span>' if p.get('label') else '') + '</div>' for p in c.get('panels', []))
    hero = c.get('hero')
    if hero:  # full-width uncropped shot; hero["fg"] = same frame with depth alpha -> sits IN FRONT of the title
        ht = hero.get('top', 300); hh = 608
        body = (f'<div class="shot" style="top:{ht}px;height:{hh}px;background-image:url(/_build/gta/{hero["img"]})"></div>'
                + f'<div class="k" style="top:{hero.get("k_top", 300)}px">{E(c["kicker"])}</div>'
                + f'<div class="big fit" style="top:{hero["title_top"]}px" data-size="{c.get("size", 250)}" data-max="1000">{c["big"]}</div>'
                + f'<div class="fg m" style="top:{ht}px;height:{hh}px;background-image:url(/_build/gta/{hero["fg"]})"></div>'
                + f'<div class="neon fit" style="top:{c.get("neon_top", 960)}px" data-size="104" data-max="700">{E(c["neon"])}</div>'
                + ''.join(f'<div class="body" style="top:{t}px">{x}</div>' for t, x in c.get('lines', []))
                + f'<div class="swipe" style="top:1292px">{c.get("swipe", "SWIPE <b>›</b>")}</div>')
        return base(body, d, amb=c.get('amb'), cover=True)
    body = ((f'<div class="shot" style="top:0;height:608px;opacity:.6;background-image:url(/_build/gta/{c["bgshot"]})"></div>' if c.get('bgshot') else '')
            + f'<div class="sun" style="right:-90px;top:{c.get("sun_top", 420)}px;width:640px;height:640px"></div>'
            + panels
            + (f'<img class="cut" src="/_build/gta/{cut["img"]}" style="right:{cut.get("right", -40)}px;top:{cut.get("top", 300)}px;height:{cut.get("h", 1100)}px">' if cut else '')
            + f'<div class="k" style="top:300px">{E(c["kicker"])}</div>'
            + f'<div class="h fit" style="top:340px" data-size="{c.get("size", 176)}" data-max="960">{c["big"]}</div>'
            + f'<div class="neon fit" style="top:{c.get("neon_top", 515)}px" data-size="104" data-max="640">{E(c["neon"])}</div>'
            + f'<div class="swipe" style="top:1292px">{c.get("swipe", "SWIPE <b>›</b>")}</div>')
    return base(body, d, amb=c.get('amb'), cover=True)


def tip(s, d, i, total):
    from PIL import Image
    if s.get('char'):
        return char(s, d, i, total)
    iw, ih = Image.open(os.path.join(R.HERE, '_build', 'gta', s['shot'])).size
    h = round(1080 * ih / iw)
    top = 230
    y = top + h - 120
    facts = ''
    if s.get('facts'):
        facts = '<div class="facts" style="top:{0}px">'.format(y + 370) + ''.join(f'<div><small>{E(a)}</small><strong>{E(b)}</strong><p>{E(c)}</p></div>' for a, b, c in s['facts']) + '</div>'
    ix = 'right:40px' if s.get('idx_right') else ''
    v4 = d.get('style', 'v4') == 'v4'  # v4 = standard since 11.11.2026 (user: "Neuer Standard"); "style": "v3" for the old look
    loc = s.get('loc') or LOC.get(s['shot'].replace('.jpg', ''))
    body = (f'<div class="shot" style="top:{top}px;height:{h}px;background-image:url(/_build/gta/{s["shot"]})"></div>'
            + (f'<div class="card" style="top:{y + 140}px"></div>' if v4 else '')
            + (f'<div class="loc" style="top:{top + 34}px"><i></i>{E(loc)}</div>' if v4 and loc else '')
            + f'<div class="idx {"fill" if s.get("fill_idx", True) else ""}" style="top:{y - 40 + s.get("idx_dy", 0)}px;font-size:250px;{ix}{';left:auto' if ix else ''}">{i:02d}</div>'
            + (f'<div class="fg" style="top:{top}px;height:{h}px;background-image:url(/_build/gta/{s["pop"]})"></div>' if s.get('pop') else '')
            + f'<div class="k" style="top:{y + 175}px">{E(s["kicker"])}</div>'
            + f'<div class="h fit" style="top:{y + 212}px" data-size="128" data-max="960">{s["title"]}</div>'
            + (f'<div class="body" style="top:{y + 345}px">{s["body"]}</div>' if s.get('body') else '')
            + facts)
    return base(body, d, amb=s['shot'].replace('.jpg', '_amb.jpg'), idx=i - 1, total=total)


def char(s, d, i, total):
    """Character slide: giant name BEHIND a BiRefNet cut-out, short text below."""
    c = s['char']
    body = (f'<div class="sun" style="left:{c.get("sun_x", 520)}px;top:{c.get("sun_top", 300)}px;width:560px;height:560px"></div>'
            + f'<div class="big fit" style="top:{c.get("name_top", 290)}px" data-size="{c.get("name_size", 330)}" data-max="1010">{E(c["name"])}</div>'
            + f'<img class="cut" src="/_build/gta/{c["img"]}" style="left:{c.get("left", -60)}px;top:{c.get("top", 420)}px;height:{c.get("h", 560)}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 14%,#000 62%,transparent 97%)">'
            + f'<div class="k" style="top:{c.get("k_top", 1030)}px">{E(s["kicker"])}</div>'
            + f'<div class="h fit" style="top:{c.get("k_top", 1030) + 37}px" data-size="104" data-max="960">{s["title"]}</div>'
            + (f'<div class="body" style="top:{c.get("k_top", 1030) + 150}px">{s["body"]}</div>' if s.get('body') else ''))
    return base(body, d, amb=s.get('amb'), idx=i - 1, total=total)


def cta(d):
    c = d['cta']
    cut = c.get('cutout')
    body = (f'<div class="sun" style="right:-160px;top:560px;width:640px;height:640px"></div>'
            + (f'<img class="cut" src="/_build/gta/{cut["img"]}" style="right:{cut.get("right", -60)}px;top:{cut.get("top", 560)}px;height:{cut.get("h", 860)}px">' if cut else '')
            + f'<div class="h fit" style="top:250px" data-size="150" data-max="960">{c["title"]}</div>'
            + f'<div class="neon fit" style="top:560px" data-size="96" data-max="560">{E(c["neon"])}</div>'
            + '<div class="save" style="top:780px"><small>YOUR GTA 6 CHEAT SHEET</small><strong>SAVE THIS</strong></div>'
            + '<div class="fol" style="top:1040px">FOLLOW <em>@PLAYHQTV</em></div>')
    return base(body, {**d, 'source': ''}, amb=c.get('amb'))


def main(data_path, out_dir):
    d = json.load(open(data_path))
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    n = len(d['tips'])
    pages = [('01_cover', cover(d))] + [(f'{i + 2:02d}_slide', tip(s, d, i + 1, n)) for i, s in enumerate(d['tips'])]
    pages.append((f'{len(pages) + 1:02d}_cta', cta(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageFilter
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=3)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(600)
            gap = pg.evaluate("(()=>{const s=document.querySelector('.src');if(!s)return 999;const b=Math.max(0,...[...document.querySelectorAll('.body,.facts,.h,.idx')].map(e=>e.getBoundingClientRect().bottom));return s.getBoundingClientRect().top-b})()")
            if gap < 40: print(f'WARN {nm}: source line only {round(gap)}px below the content')
            raw = os.path.join(tmp, nm + '@3x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=2))
            R.save_jpg(im, os.path.join(out_dir, nm + '.jpg')); print(os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
