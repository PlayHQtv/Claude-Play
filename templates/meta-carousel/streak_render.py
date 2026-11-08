"""PlayHQ "EVERY MW4 KILLSTREAK" reference carousel (design v3 HUD, same look as poi_render).
Usage: python3 streak_render.py data/<file>.json [out_dir] -> cover, one slide per kill tier, rules slide, cta. 1080x1440."""
import json, os, sys
import render as R
import poi_render as P

E = R.E
CSS_EXTRA = """
.sk{display:flex;align-items:center;gap:22px;padding:16px 20px 16px 16px}
.sk .k{flex:none;width:140px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);color:#140f00;clip-path:polygon(0 0,100% 0,100% 78%,78% 100%,0 100%)}
.sk .k b{font-family:Anton;font-weight:400;font-size:78px;line-height:1}
.sk .k small{font-weight:700;font-size:19px;letter-spacing:4px}
.sk.nuke .k{background:linear-gradient(135deg,#ff8a7a,#ff4b3e 55%,#a51d12);color:#fff}
.sk .tx{flex:1;min-width:0}
.sk .im{flex:none;width:270px;height:152px;background-size:cover;background-position:center;position:relative;border:2px solid rgba(255,212,0,.55);clip-path:polygon(0 0,100% 0,100% 82%,88% 100%,0 100%)}
.sk .kb{position:absolute;left:0;top:0;width:86px;height:86px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);color:#140f00;clip-path:polygon(0 0,100% 0,100% 74%,74% 100%,0 100%)}
.sk .kb b{font-family:Anton;font-weight:400;font-size:52px;line-height:1}
.sk .kb small{font-weight:700;font-size:13px;letter-spacing:3px}
.sk .k{height:152px}
.sk .hd{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.sk .nm{font-family:Anton;font-size:48px;line-height:1.05;letter-spacing:1px;color:#f3f3f3}
.sk .lv{font-weight:700;font-size:20px;letter-spacing:3px;color:#111;background:#3ddc84;padding:3px 10px}
.sk .nt{font-weight:700;font-size:20px;letter-spacing:3px;color:var(--y);border:1px solid rgba(255,212,0,.5);padding:2px 9px}
.sk p{font-weight:600;font-size:29px;line-height:1.25;color:#d9d9d9;margin-top:6px}
.ru{display:flex;gap:24px;align-items:flex-start;padding:24px 26px}
.ru b{flex:none;width:260px;font-family:Anton;font-weight:400;font-size:44px;line-height:1.1;color:var(--y)}
.ru p{font-weight:600;font-size:33px;line-height:1.28;color:#e2e2e2}
.cv .rg{font-size:20px}.cv .ch{font-size:30px;padding:6px 14px 6px 8px}.cv .ch i{font-size:19px}
.th{position:absolute;left:50px;width:885px;display:flex;gap:16px}
.th>div{flex:1}.th .ti{height:150px;background-size:cover;background-position:center;border:2px solid rgba(255,212,0,.6);clip-path:polygon(0 0,100% 0,100% 84%,90% 100%,0 100%)}
.th b{display:block;font-family:Anton;font-weight:400;font-size:30px;letter-spacing:1px;color:#f1f1f1;margin-top:8px}
.st{position:absolute;left:50px;width:885px;display:flex;gap:12px}
.st span{flex:1;text-align:center;font-family:Anton;font-size:40px;letter-spacing:1px;padding:22px 6px;color:#f1f1f1}
"""


def page(body, d):
    return P.page(body, d).replace('</style>', CSS_EXTRA + '</style>', 1)


def card(s):
    lv = f'<span class="lv">UNLOCK LV {s["lv"]}</span>' if s.get('lv') else ''
    nt = f'<span class="nt">{E(s["note"])}</span>' if s.get('note') else ''
    vis = (f'<div class="im" style="background-image:url(/_build/ks/{s["img"]}.jpg)"><div class="kb"><b>{E(s["kills"])}</b><small>KILLS</small></div></div>'
           if s.get('img') else f'<div class="k"><b>{E(s["kills"])}</b><small>KILLS</small></div>')
    return (f'<div class="pc hud sk{" nuke" if s.get("nuke") else ""}">{vis}'
            f'<div class="tx"><div class="hd"><span class="nm">{E(s["name"].upper())}</span>{lv}{nt}</div><p>{E(s["desc"])}</p></div></div>')


def tier_slide(t, d):
    body = (f'<div class="sec">{E(t["sub"])}</div><div class="fit" style="top:240px" data-size="96" data-max="860"><span class="gr w">{E(t["title"])}</span></div>'
            + '<div class="stack" style="top:370px;gap:20px">' + ''.join(card(s) for s in t['streaks']) + '</div>')
    return page(body, {**d, 'footer': ''})


def rules_slide(d):
    r = d['rules']
    body = (f'<div class="sec">{E(r["sub"])}</div><div class="fit" style="top:240px" data-size="110" data-max="860"><span class="gr gold">{E(r["title"])}</span></div>'
            + '<div class="stack" style="top:390px;gap:20px">' + ''.join(f'<div class="pc hud ru"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in r['items']) + '</div>')
    return page(body, {**d, 'footer': ''})


def cover_slide(d):
    c = d['cover']
    tiers = ''.join(f'<span class="hud">{k}</span>' for k in ('4–5', '6', '8', '10', '12', 'NUKE'))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="210" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:470px" data-size="120" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:610px;left:62px;font-size:23px;letter-spacing:5px;color:#d9d9d9">{E(c["sub"])}</div>'
            + f'<div class="sec" style="top:690px">KILL TIERS</div><div class="st" style="top:735px">{tiers}</div>'
            + '<div class="sec" style="top:868px">UNLOCKED FIRST · LEVEL 4</div><div class="th" style="top:905px">'
            + ''.join(f'<div><div class="ti" style="background-image:url(/_build/ks/{n.lower().replace(" ", "-")}.jpg)"></div><b>{E(n.upper())}</b></div>' for n in c['start']) + '</div>'
            + '<div class="pc hud cv" style="top:1118px"><div class="rg">PRO TIP</div><div class="nm" style="font-family:Raj;font-weight:700;font-size:36px">Hardline makes every streak 1 kill cheaper</div></div>'
            + f'<div class="swipe" style="top:1250px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': ''})


def cta_slide(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:215px" data-size="140" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:365px" data-size="140" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:530px;left:60px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + '<div class="pc hud" style="top:600px"><div class="rg">EXAMPLE</div><div class="nm" style="font-family:Raj;font-weight:700;font-size:34px">UAV (5) · Counter UAV (6) · Wheelson (8)</div></div>'
            + '<div class="t hud save" style="position:absolute;left:150px;width:640px;top:800px;height:130px;justify-content:center"><div class="tx" style="text-align:center;padding:0"><small style="font-size:20px">YOUR STREAK CHEAT SHEET</small><b style="font-size:60px">SAVE THIS</b></div></div>'
            + '<img src="/assets/logo.png" style="position:absolute;left:60px;top:990px;width:120px">'
            + '<div style="position:absolute;left:205px;top:1002px;font-family:Anton;font-size:62px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div style="position:absolute;left:207px;top:1075px;font-weight:700;color:#cfcfcf;letter-spacing:6px;font-size:22px">{E(c["follow_sub"])}</div>')
    return page(body, {**d, 'footer': ''})


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    out_dir = out_dir or os.path.join(R.HERE, 'out', os.path.splitext(os.path.basename(data_path))[0])
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover_slide(d))]
    for t in d['tiers']:
        pages.append((f'{len(pages) + 1:02d}_tier', tier_slide(t, d)))
    pages.append((f'{len(pages) + 1:02d}_rules', rules_slide(d)))
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
            bot = pg.evaluate("Math.max(...[...document.querySelectorAll('.stack')].map(e=>e.getBoundingClientRect().bottom),0)")
            print(nm, 'stack bottom', round(bot))
            raw = os.path.join(tmp, nm + '@2x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
            R.save_jpg(im, os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
