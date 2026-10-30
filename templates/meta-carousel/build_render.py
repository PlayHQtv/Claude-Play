"""PlayHQ single-weapon build carousel ("Best <gun> build MW4"), design v3 HUD.
Usage: python3 build_render.py data/<file>.json [out_dir]
Slides: cover (one big weapon), one slide per build (render.weapon_slide), cta (render.cta_slide). 1080x1440."""
import json, os, sys
import render as R

E = R.E


def cover_slide(d):
    c = d['cover']
    rows = ''.join(f'<div class="row hud" style="top:{880 + i * 84}px;height:74px"><div class="n" style="font-size:48px">{w["rank"]}</div>'
                   f'<b style="font-size:32px">{E(w["short"])}</b><small>{E(w["build_code"])}</small></div>' for i, w in enumerate(d['weapons']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:240px" data-size="170" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:420px" data-size="120" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:552px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + '<div class="floor" style="top:880px"></div><div class="line" style="top:897px"></div>'
            + f'<div class="gunbox" style="top:600px;height:290px;width:900px"><img class="gun" style="max-height:270px;max-width:860px;filter:drop-shadow(0 40px 30px rgba(0,0,0,.85)) brightness(1.2) contrast(1.08)" src="/weapons/{c["image"]}"></div>'
            + rows + f'<div class="swipe" style="top:1222px;font-size:26px;right:110px">{E(c["swipe"])}</div>')
    return R.page(body, {**d, 'footer': ''})


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    out_dir = out_dir or os.path.join(R.HERE, 'out', os.path.splitext(os.path.basename(data_path))[0])
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover_slide(d))]
    for w in d['weapons']:
        pages.append((f'{len(pages) + 1:02d}_build_{w["rank"]}', R.weapon_slide(w, d)))
    pages.append((f'{len(pages) + 1:02d}_cta', R.cta_slide(d)))
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
