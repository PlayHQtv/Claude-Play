"""PlayHQ "EVERY POI THREAT LEVEL" list carousel (design v3 HUD).
Usage: python3 poi_render.py data/<file>.json [out_dir]  -> cover, list slides (POI cards with colour-coded threat chips), cta. 1080x1440."""
import json, os, sys
import render as R

E = R.E
COL = {"Low": "#3ddc84", "Medium": "#ffd400", "High": "#ff9a1f", "Critical": "#ff4b3e", "Extreme": "#c04bff"}
CSS_EXTRA = """
.sec{position:absolute;left:60px;top:205px;font-weight:700;font-size:24px;letter-spacing:8px;color:var(--y)}
.pc{position:absolute;left:50px;width:885px;padding:14px 22px 14px 24px}
.stack{position:absolute;left:50px;top:340px;width:885px;display:flex;flex-direction:column;gap:14px}
.stack .pc{position:relative;left:0;top:auto}
.pc.pi{display:flex;gap:20px;align-items:center;padding:12px 18px 12px 12px}
.pc.pi .im{flex:none;width:272px;height:136px;background-size:100% 100%;border:2px solid rgba(255,212,0,.55);clip-path:polygon(0 0,100% 0,100% 82%,88% 100%,0 100%)}
.pc.pi .tx{flex:1;min-width:0}
.pc.pi .ch{font-size:22px}
.pmap{position:absolute;left:50px;width:885px;border:2px solid rgba(255,212,0,.6);background-size:100% 100%;clip-path:polygon(0 0,100% 0,100% 90%,94% 100%,0 100%)}
.pc .nm{font-family:Anton;font-size:40px;line-height:1.05;letter-spacing:1px;color:#f1f1f1}
.pc .rg{font-weight:700;font-size:17px;letter-spacing:4px;color:#9a9a9a;margin:2px 0 8px}
.pc .ar{display:flex;flex-wrap:wrap;gap:8px 10px}
.ch{display:flex;align-items:center;gap:8px;font-weight:600;font-size:22px;color:#e6e6e6;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);padding:3px 10px 3px 8px}
.ch i{font-style:normal;font-weight:700;font-size:16px;letter-spacing:2px;padding:2px 8px;color:#111}
.lg{position:absolute;left:50px;width:885px;display:flex;gap:10px;justify-content:space-between}
.lg span{flex:1;text-align:center;font-weight:700;font-size:20px;letter-spacing:2px;color:#111;padding:8px 0}
"""


def page(body, d):
    return R.page(body, d).replace('</style>', CSS_EXTRA + '</style>', 1)


def chip(a, lvl):
    return f'<span class="ch"><i style="background:{COL[lvl]}">{lvl.upper()}</i>{E(a)}</span>'


def card(p, top):
    img = f'<div class="im" style="background-image:url(/_build/s1/{p["img"]})"></div>' if p.get('img') else ''
    return (f'<div class="pc hud{" pi" if img else ""}">{img}<div class="tx"><div class="nm">{E(p["name"].upper())}</div><div class="rg">{E(p["region"].upper())}</div>'
            f'<div class="ar">{"".join(chip(a, l) for a, l in p["areas"])}</div></div></div>')


def legend(top):
    return '<div class="lg" style="top:%dpx">%s</div>' % (top, ''.join(f'<span style="background:{c}">{k.upper()}</span>' for k, c in COL.items()))


def list_slide(ps, sub, title, d):
    body = (f'<div class="sec">{E(sub)}</div><div class="fit" style="top:240px" data-size="84" data-max="860"><span class="gr w">{E(title)}</span></div>'
            + '<div class="stack">' + ''.join(card(p, 0) for p in ps)
            + (''.join(f'<div class="pc hud"><div class="rg" style="color:var(--y)">{E(a)}</div><div class="nm" style="font-family:Raj;font-weight:700;font-size:32px;line-height:1.25">{E(b)}</div></div>' for a, b in d.get('notes_box', [])) if len(ps) < 5 else '')
            + '</div>')
    return page(body, {**d, 'footer': ''}), 0


def cover_slide(d):
    c = d['cover']
    if c.get('img'):  # v2: official tactical map, shown complete
        from PIL import Image
        iw, ih = Image.open(os.path.join(R.HERE, '_build', 's1', c['img'])).size
        h = round(885 * ih / iw)
        mid = (f'<div class="pmap" style="top:665px;height:{h}px;background-image:url(/_build/s1/{c["img"]})"></div>' + legend(665 + h + 26))
        sw = 665 + h + 26 + 70
    else:
        mid = (legend(700)
               + '<div class="pc hud" style="top:790px"><div class="rg">SAFEST DROP</div><div class="ar">' + chip("Songdo Wharf", "Low") + chip("Mirae General Hospital", "Low") + '</div></div>'
               + '<div class="pc hud" style="top:960px"><div class="rg">MOST DANGEROUS</div><div class="ar">' + chip("Air Base Bunker", "Extreme") + chip("Nenshin Tech Complex", "Extreme") + '</div></div>')
        sw = 1170
    pre = ''
    if c.get('cutout'):  # free-standing operator BEHIND the title (rembg/ISNet cut-out, graded), fades out into the map
        k = c['cutout']
        pre = (f'<img src="/_build/s1/{k["img"]}" style="position:absolute;right:{k.get("right", 0)}px;top:{k["top"]}px;width:{k["w"]}px;'
               '-webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 98%);'
               'filter:drop-shadow(-22px 12px 30px rgba(0,0,0,.9)) brightness(1.04)">')
    body = (pre + f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="200" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:460px" data-size="130" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:610px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + mid + f'<div class="swipe" style="top:{sw}px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': '', 'cover_logo': 1})


def cta_slide(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:215px" data-size="140" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:365px" data-size="140" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:530px;left:60px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + f'<div class="pc hud" style="top:600px"><div class="rg">GOOD TO KNOW</div><div class="nm" style="font-family:Raj;font-weight:700;font-size:34px">{E(d["tip"])}</div></div>'
            + '<div class="t hud save" style="position:absolute;left:150px;width:640px;top:800px;height:130px;justify-content:center"><div class="tx" style="text-align:center;padding:0"><small style="font-size:20px">CHECK IT BEFORE YOU DROP</small><b style="font-size:60px">SAVE THIS</b></div></div>'
            + '<img src="/assets/logo.png" style="position:absolute;left:60px;top:990px;width:120px">'
            + '<div style="position:absolute;left:205px;top:1002px;font-family:Anton;font-size:62px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div style="position:absolute;left:207px;top:1075px;font-weight:700;color:#cfcfcf;letter-spacing:6px;font-size:22px">{E(c["follow_sub"])}</div>')
    return page(body, {**d, 'footer': ''})


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    out_dir = out_dir or os.path.join(R.HERE, 'out', os.path.splitext(os.path.basename(data_path))[0])
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    P = d['pois']
    groups = [(P[0:5], 'STARTS LOW · WATCH THE HOTSPOTS'), (P[5:10], 'STARTS MEDIUM · SOME RISK'), (P[10:13], 'HIGH TO EXTREME · LOOT + DANGER')]
    pages = [('01_cover', cover_slide(d))]
    n = 0
    for g, title in groups:
        h, bottom = list_slide(g, f'MW4 DMZ POIS {n + 1:02d}–{n + len(g):02d} OF 13', title, d)
        print('bottom', bottom)
        n += len(g)
        pages.append((f'{len(pages) + 1:02d}_pois', h))
    for x in d.get('extra_slides', []):  # e.g. X01 (s1_render hero + rules layout)
        import s1_render
        pages.append((f'{len(pages) + 1:02d}_extra', s1_render.slide(x, d)))
    pages.append((f'{len(pages) + 1:02d}_cta', cta_slide(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageFilter
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=3)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(300)
            raw = os.path.join(tmp, nm + '@3x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
            R.save_jpg(im, os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
