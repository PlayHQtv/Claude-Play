"""PlayHQ "MISTAKES" carousel (tips format, design v3 HUD).
Usage: python3 mistakes_render.py data/<file>.json [out_dir]
Slides: cover, one slide per mistake (DON'T / DO THIS box + gold line icon), cta. 1080x1440 (3:4) JPG.
Reuses CSS, frame, auto-fit and the 2x render pipeline from render.py / apex_render.py."""
import json, os, sys
import render as R

E = R.E
CSS_EXTRA = """
:root{--r:#ff4b3e}
.mk{position:absolute;left:60px;top:200px;display:flex;align-items:center;gap:16px;font-weight:700;font-size:28px;letter-spacing:8px}
.mk .tag{background:var(--r);color:#fff;padding:2px 14px 0;font-family:Anton;font-weight:400;letter-spacing:3px;font-size:28px;line-height:42px}
.mk .no{color:var(--y)}
.mk .pt{color:#9a9a9a;font-size:22px;letter-spacing:6px}
.pan{position:absolute;left:50px;width:885px}
.ill{top:500px;height:360px;display:grid;place-items:center}
.ill img{width:560px;position:relative;z-index:1}
.ill .big{position:absolute;right:30px;bottom:-14px;font-family:Anton;font-size:230px;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(255,212,0,.16)}
.ill .glow{position:absolute;inset:0;background:radial-gradient(ellipse 380px 160px at 50% 55%,rgba(255,212,0,.12),transparent 70%)}
.box{display:flex;align-items:center;gap:26px;padding:0 34px 0 28px}
.box .b{flex:none;width:74px;height:74px;display:grid;place-items:center;font-family:Anton;font-size:46px;line-height:1;clip-path:polygon(0 0,100% 0,100% 72%,72% 100%,0 100%)}
.box small{display:block;font-weight:700;font-size:20px;letter-spacing:6px;margin-bottom:6px}
.box p{font-weight:600;font-size:31px;line-height:1.2;color:#ececec}
.dont{top:885px;height:150px;border-color:rgba(255,75,62,.45)}
.dont::after{background:var(--r);box-shadow:0 0 10px rgba(255,75,62,.7)}
.dont .b{background:var(--r);color:#fff}
.dont small{color:var(--r)}
.dont p{color:#cfcfcf}
.do{top:1050px;height:200px;border-color:rgba(255,212,0,.55);background:linear-gradient(180deg,rgba(40,33,8,.95),rgba(14,12,6,.95))}
.do .b{background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);color:#140f00}
.do small{color:var(--y)}
.do p{color:#fff;font-size:32px}
.chips{position:absolute;left:50px;width:885px;top:640px;display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.chip{height:190px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.chip img{width:150px}
.chip b{font-family:Anton;font-weight:400;font-size:40px;letter-spacing:2px;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.p1{position:absolute;left:50px;width:885px;top:880px;height:250px;padding:28px 34px}
.p1 small{display:block;font-weight:700;font-size:20px;letter-spacing:6px;color:#9a9a9a;margin-bottom:12px}
.p1 p{font-weight:600;font-size:30px;line-height:1.35;color:#d6d6d6}
.p1 p s{text-decoration:none;color:var(--y)}
"""


def page(body, d):
    return R.page(body, d).replace('</style>', CSS_EXTRA + '</style>', 1)


def mistake_slide(m, d):
    tw, tg = m['title_white'], m['title_gold']
    body = (f'<div class="mk"><span class="tag">MISTAKE</span><span class="no">#{m["n"]:02d}</span><span class="pt">· {E(d["series"])}</span></div>'
            + f'<div class="fit" style="top:255px" data-size="118" data-max="850"><span class="gr w">{E(tw)}</span></div>'
            + f'<div class="fit" style="top:378px" data-size="118" data-max="850"><span class="gr gold">{E(tg)}</span></div>'
            + f'<div class="pan hud ill"><div class="glow"></div><div class="big">{m["n"]:02d}</div><img src="/assets/icons/m_{m["icon"]}.svg"></div>'
            + f'<div class="pan hud box dont"><div class="b">✕</div><div><small>DON\'T</small><p>{E(m["dont"])}</p></div></div>'
            + f'<div class="pan hud box do"><div class="b">✓</div><div><small>DO THIS INSTEAD</small><p>{E(m["do"])}</p></div></div>')
    return page(body, {**d, 'footer': ''})


def cover_slide(d):
    c = d['cover']
    chips = ''.join(f'<div class="chip hud"><img src="/assets/icons/m_{m["icon"]}.svg"><b>#{m["n"]:02d}</b></div>' for m in d['mistakes'])
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="210" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:470px" data-size="110" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:592px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + f'<div class="chips" style="top:650px">{chips}</div>'
            + '<div class="p1 hud" style="top:870px;height:250px"><small>MISSED PART 1?</small>'
            + '<p>#01 Two guns · #02 Knife out · #03 The 50K gun<br>#04 Keys too early · #05 Skipping crate boxes<br><s>It\'s on our profile.</s></p></div>'
            + f'<div class="swipe" style="top:1180px;font-size:30px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': ''})


def cta_slide(d):
    c = d['cta']
    rows = ''.join(
        f'<div class="row hud" style="top:{560 + i * 104}px;height:92px"><div class="n" style="width:96px;font-size:50px">{m["n"]:02d}</div>'
        f'<img src="/assets/icons/m_{m["icon"]}.svg" style="width:120px;filter:none"><b style="font-size:30px">{E(m["short"])}</b></div>'
        for i, m in enumerate(d['mistakes']))
    body = (f'<div class="fit" style="top:205px" data-size="140" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:355px" data-size="140" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:510px;left:60px;font-size:24px;letter-spacing:7px;color:#d9d9d9">{E(c["sub"])}</div>'
            + rows
            + '<img src="/assets/logo.png" style="position:absolute;left:60px;top:1100px;width:120px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.7))">'
            + '<div style="position:absolute;left:205px;top:1112px;font-family:Anton;font-size:62px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div style="position:absolute;left:207px;top:1185px;font-weight:700;color:#cfcfcf;letter-spacing:6px;font-size:22px">{E(c["follow_sub"])}</div>')
    return page(body, {**d, 'footer': ''})


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    name = os.path.splitext(os.path.basename(data_path))[0]
    out_dir = out_dir or os.path.join(R.HERE, 'out', name)
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover_slide(d))]
    for m in d['mistakes']:
        pages.append((f'{len(pages) + 1:02d}_mistake_{m["n"]:02d}', mistake_slide(m, d)))
    pages.append((f'{len(pages) + 1:02d}_cta', cta_slide(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageFilter
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=2)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(300)
            raw = os.path.join(tmp, nm + '@2x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
            im.save(os.path.join(out_dir, nm + '.jpg'), 'JPEG', quality=95, subsampling=0, optimize=True)
            print(os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
