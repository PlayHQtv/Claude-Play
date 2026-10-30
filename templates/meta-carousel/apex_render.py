"""PlayHQ "EVERY APEX" carousel (list format, design v3).
Usage: python3 apex_render.py data/<file>.json [out_dir]
Slides: cover, 7 list slides with 4 apex cards each, cta. 1080x1440 (3:4) JPG.
Reuses the CSS, frame, auto-fit and 2x render pipeline from render.py."""
import json, os, sys
import render as R

E = R.E
CSS_EXTRA = """
.sec{position:absolute;left:60px;top:205px;font-weight:700;font-size:26px;letter-spacing:9px;color:var(--y)}
.ac{position:absolute;left:50px;width:885px;height:208px}
.ac .im{position:absolute;left:14px;top:14px;width:330px;height:180px;display:grid;place-items:center;
  background:radial-gradient(ellipse at 50% 60%,rgba(255,212,0,.13),transparent 70%)}
.ac .im img{max-width:318px;max-height:150px;filter:drop-shadow(0 14px 10px rgba(0,0,0,.85)) brightness(1.18) contrast(1.06)}
.ac .ix{position:absolute;left:362px;top:20px;font-weight:700;font-size:17px;letter-spacing:4px;color:rgba(255,212,0,.7)}
.ac .ix b{color:#cfcfcf;font-weight:700;margin-left:10px}
.ac .nm{position:absolute;left:360px;top:44px;font-family:Anton;line-height:1.05;white-space:nowrap;letter-spacing:1px}
.ac .ef{position:absolute;left:362px;top:112px;width:490px;font-weight:600;font-size:25px;line-height:1.18;color:#e2e2e2}
.ac .lv{position:absolute;right:26px;top:16px;font-weight:700;font-size:15px;letter-spacing:3px;color:#9a9a9a;text-align:right}
.ac .lv b{display:block;font-family:Anton;font-weight:400;font-size:30px;letter-spacing:1px;color:var(--y);line-height:1}
"""


def page(body, d):
    return R.page(body, d).replace('</style>', CSS_EXTRA + '</style>', 1)


def card(it, top):
    return (f'<div class="ac hud" style="top:{top}px">'
            f'<div class="im"><img src="/weapons/{it["image"]}"></div>'
            f'<div class="ix">{it["n"]:02d}/28<b>{E(it["weapon"].upper())} · {E(SHORT[it["cls"]])}</b></div>'
            f'<div class="nm fit gold" style="left:360px" data-size="50" data-max="390"><span class="gold">{E(it["apex"].upper())}</span></div>'
            f'<div class="lv">MAX LVL<b>{it["level"]}</b></div>'
            f'<div class="ef">{E(it["effect"])}</div></div>')


def list_slide(items, title, sub, d):
    body = (f'<div class="sec">{E(sub)}</div>'
            + f'<div class="fit" style="top:245px" data-size="86" data-max="860"><span class="gr w">{E(title)}</span></div>'
            + ''.join(card(it, 360 + i * 222) for i, it in enumerate(items)))
    return page(body, {**d, 'footer': ''})


def cover_slide(d):
    c = d['cover']
    by = {it['apex']: it for it in d['items']}
    pos = [(50, 640), (500, 640), (50, 920), (500, 920)]
    cards = ''.join(
        f'<div class="card hud" style="left:{x}px;top:{y}px">'
        f'<div class="cimg" style="top:18px;height:150px"><img src="/weapons/{by[a]["image"]}" style="max-height:150px;filter:drop-shadow(0 16px 12px rgba(0,0,0,.8)) brightness(1.18)"></div>'
        f'<div style="position:absolute;left:22px;bottom:58px;font-weight:700;font-size:15px;letter-spacing:4px;color:#bdbdbd">{E(by[a]["weapon"].upper())} APEX</div>'
        f'<div class="nm fit" style="left:22px;top:auto;bottom:20px;position:absolute" data-size="30" data-max="390"><span class="gold" style="font-family:Raj;font-weight:700">{E(a.upper())}</span></div></div>'
        for (x, y), a in zip(pos, c['show']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:240px" data-size="200" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:455px" data-size="120" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:592px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + cards + f'<div class="swipe" style="top:1200px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': ''})


def cta_slide(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:215px" data-size="140" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:365px" data-size="140" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:530px;left:60px;font-size:26px;letter-spacing:7px;color:#d9d9d9">{E(c["sub"])}</div>'
            + '<div class="t hud save" style="position:absolute;left:150px;width:640px;top:650px;height:150px;justify-content:center"><div class="tx" style="text-align:center;padding:0"><small style="font-size:20px">DON\'T LOSE THE LIST</small><b style="font-size:64px">SAVE THIS</b></div></div>'
            + '<img src="/assets/logo.png" style="position:absolute;left:420px;top:870px;width:150px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.7))">'
            + '<div style="position:absolute;left:0;right:100px;top:1050px;text-align:center;font-family:Anton;font-size:72px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div class="swipe" style="top:1140px;color:#cfcfcf;letter-spacing:7px;font-size:24px;right:100px">{E(c["follow_sub"])}</div>')
    return page(body, {**d, 'footer': ''})


SHORT = {'ASSAULT RIFLE': 'AR', 'SMG': 'SMG', 'SHOTGUN': 'SHOTGUN', 'LMG': 'LMG', 'MARKSMAN RIFLE': 'DMR', 'SNIPER RIFLE': 'SNIPER', 'PISTOL': 'PISTOL'}
TITLES = {'ASSAULT RIFLE': 'ASSAULT RIFLES', 'SMG': 'SMGS', 'SHOTGUN': 'SHOTGUNS', 'LMG': 'LMGS',
          'MARKSMAN RIFLE': 'MARKSMAN RIFLES', 'SNIPER RIFLE': 'SNIPERS', 'PISTOL': 'PISTOLS'}


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    name = os.path.splitext(os.path.basename(data_path))[0]
    out_dir = out_dir or os.path.join(R.HERE, 'out', name)
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover_slide(d))]
    items = d['items']
    for k in range(0, len(items), 4):
        grp = items[k:k + 4]
        classes = list(dict.fromkeys(TITLES[i['cls']] for i in grp))
        title = ' + '.join(classes)
        sub = f'EVERY APEX IN MW4 · {grp[0]["n"]:02d}–{grp[-1]["n"]:02d} OF 28'
        pages.append((f'{len(pages) + 1:02d}_apex_{grp[0]["n"]:02d}', list_slide(grp, title, sub, d)))
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
