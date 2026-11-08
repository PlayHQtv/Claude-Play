"""PlayHQ season/news carousel (design v3 HUD, image cards like streak_render).
Usage: python3 s1_render.py data/<file>.json [out_dir]. Images are read from _build/s1/ (private, never committed)."""
import json, os, sys
import render as R
import streak_render as S

E = R.E
CSS = """
.s1c{display:flex;align-items:center;gap:22px;padding:14px 20px 14px 14px}
.s1c .im{flex:none;width:270px;height:150px;background-size:cover;background-position:center;border:2px solid rgba(255,212,0,.55);clip-path:polygon(0 0,100% 0,100% 82%,88% 100%,0 100%)}
.s1c .im.ct{background-size:contain;background-repeat:no-repeat;background-color:rgba(255,255,255,.04)}
.s1c .im.dk{background-color:#0b0b0b;background-size:120px}
.s1c .tx{flex:1;min-width:0}
.s1c .hd{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.s1c .nm{font-family:Anton;font-size:46px;line-height:1.05;color:#f3f3f3}
.s1c .cp{font-weight:700;font-size:19px;letter-spacing:3px;color:#111;background:#3ddc84;padding:3px 10px}
.s1c .cp.ng{background:#ff4b3e;color:#fff}
.s1c p{font-weight:600;font-size:28px;line-height:1.25;color:#d9d9d9;margin-top:6px}
.s1c.cm{padding:10px 18px 10px 12px}.s1c.cm .im{height:118px;width:236px}.s1c.cm .nm{font-size:42px}.s1c.cm p{font-size:26px;margin-top:3px}
.s1ft{position:absolute;left:50px;width:885px;font-weight:700;font-size:22px;letter-spacing:4px;color:var(--y);text-align:center}
.s1hero{position:absolute;left:50px;width:885px;height:400px;background-size:cover;background-position:center;border:2px solid rgba(255,212,0,.6);clip-path:polygon(0 0,100% 0,100% 90%,94% 100%,0 100%)}
.cv2 .ch2{display:flex;gap:12px;position:absolute;left:50px;width:885px}
.cv2 .ch2 span{flex:1;text-align:center;font-family:Anton;font-size:30px;padding:16px 4px;color:#f1f1f1}
"""


def hero(img, top, maxh, maxw=885, left=50):
    """Hero image shown COMPLETE (no crop): fit the image's own aspect into maxw x maxh, centred."""
    from PIL import Image
    iw, ih = Image.open(os.path.join(R.HERE, '_build', 's1', img)).size
    w, h = maxw, round(maxw * ih / iw)
    if h > maxh:
        h, w = maxh, round(maxh * iw / ih)
    x = left + (maxw - w) // 2
    return f'<div class="s1hero hud" style="top:{top}px;left:{x}px;width:{w}px;height:{h}px;background-size:100% 100%;background-image:url(/_build/s1/{img})"></div>', h


def page(body, d):
    return S.page(body, d).replace('</style>', CSS + '</style>', 1)


def card(c, cm=False):
    cls = 'im' + (' ct' if c.get('fit') == 'contain' else '') + (' dk' if c.get('dark') else '')
    return (f'<div class="pc hud s1c{" cm" if cm else ""}"><div class="{cls}" style="background-image:url(/_build/s1/{c["img"]})"></div>'
            f'<div class="tx"><div class="hd"><span class="nm">{E(c["name"].upper())}</span><span class="cp{" ng" if c.get("neg") else ""}">{E(c["chip"])}</span></div>'
            f'<p>{E(c["desc"])}</p></div></div>')


def rules(rs):
    return ''.join(f'<div class="pc hud ru"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in rs)


def slide(s, d):
    head = f'<div class="sec">{E(s["sec"])}</div><div class="fit" style="top:240px" data-size="100" data-max="860"><span class="gr w">{E(s["title"])}</span></div>'
    if s.get('hero'):
        hh, h = hero(s['hero'], 365, s.get('hero_max', 470))
        body = head + hh + f'<div class="stack" style="top:{365 + h + 22}px;gap:10px">{rules(s["rules"])}</div>'
    else:
        inner = ''.join(card(c, len(s['cards']) >= 5) for c in s['cards']) + (rules(s['rules']) if s.get('rules') else '')
        body = head + f'<div class="stack" style="top:365px;gap:16px">{inner}</div>'
        if s.get('foot'):
            body += f'<div class="s1ft" style="top:1230px">{E(s["foot"])}</div>'
    return page(body, {**d, 'footer': ''})


def cover(d):
    c = d['cover']
    chips = ''.join(f'<span class="hud">{E(x)}</span>' for x in c['chips'])
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="190" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:450px" data-size="120" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:590px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + hero(c['img'], 650, 420)[0]
            + f'<div class="cv2"><div class="ch2" style="top:1095px">{chips}</div></div>'
            + f'<div class="swipe" style="top:1235px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': '', 'cover_logo': 1})


def cta(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:230px" data-size="130" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:375px" data-size="130" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:540px;left:60px;font-size:24px;letter-spacing:5px;color:#d9d9d9">{E(c["sub"])}</div>'
            + '<div class="t hud save" style="position:absolute;left:150px;width:640px;top:680px;height:130px;justify-content:center"><div class="tx" style="text-align:center;padding:0"><small style="font-size:20px">YOUR SEASON 1 CHEAT SHEET</small><b style="font-size:60px">SAVE THIS</b></div></div>'
            + '<img src="/assets/logo.png" style="position:absolute;left:60px;top:900px;width:120px">'
            + '<div style="position:absolute;left:205px;top:912px;font-family:Anton;font-size:62px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div style="position:absolute;left:207px;top:985px;font-weight:700;color:#cfcfcf;letter-spacing:6px;font-size:22px">{E(c["follow_sub"])}</div>')
    return page(body, {**d, 'footer': ''})


def main(data_path, out_dir):
    d = json.load(open(data_path))
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover(d))] + [(f'{i + 2:02d}_slide', slide(s, d)) for i, s in enumerate(d['slides'])]
    pages.append((f'{len(pages) + 1:02d}_cta', cta(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageFilter
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=3)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(400)
            bot = pg.evaluate("Math.max(...[...document.querySelectorAll('.stack')].map(e=>e.getBoundingClientRect().bottom),0)")
            print(nm, 'stack bottom', round(bot))
            raw = os.path.join(tmp, nm + '@3x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            R.save_jpg(im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2)), os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
