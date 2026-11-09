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
.st{display:flex;align-items:center;gap:20px;padding:18px 26px}
.st .l{flex:1;min-width:0}.st .l b{display:block;font-family:Anton;font-size:40px;line-height:1.08;color:#f3f3f3}
.st .l p{font-weight:600;font-size:25px;line-height:1.25;color:#cfcfcf;margin-top:4px}
.st .v{flex:none;max-width:330px;text-align:right;font-family:Anton;font-size:46px;line-height:1.05;color:var(--y)}
.cv2 .ch2{display:flex;gap:12px;position:absolute;left:50px;width:885px}
.cv2 .ch2 span{flex:1;text-align:center;font-family:Anton;font-size:30px;padding:16px 4px;color:#f1f1f1}
.bleed{position:absolute;left:0;width:1080px;background-size:100% 100%;box-shadow:0 30px 60px rgba(0,0,0,.6)}
.bleed::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;background:linear-gradient(90deg,var(--y),rgba(255,212,0,0))}
.bleed::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,var(--y),rgba(255,212,0,0))}
.mtag{position:absolute;right:50px;font-family:Anton;font-size:34px;letter-spacing:2px;padding:8px 18px 6px;line-height:1}
.mtag.new{background:#3ddc84;color:#0b0b0b}.mtag.old{background:rgba(255,255,255,.1);color:#f1f1f1;border:2px solid rgba(255,255,255,.45)}
.mtag.tech{background:var(--y);color:#111}
.shotcap{position:absolute;left:50px;width:870px}
.shotcap .ln{display:flex;gap:22px;align-items:baseline;margin-bottom:22px}
.shotcap .ln b{flex:none;width:215px;font-family:Anton;font-size:40px;color:var(--y);letter-spacing:1px}
.shotcap .ln p{flex:1;font-weight:600;font-size:35px;line-height:1.28;color:#e6e6e6}
.gr2{display:flex;align-items:center;gap:16px;padding:16px 22px 16px 8px}
.gr2 .gw{flex:none;width:500px;height:200px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 24px 20px rgba(0,0,0,.85))}
.gr2 .gw img{max-width:492px;max-height:192px;filter:drop-shadow(0 0 1px rgba(255,226,150,.95)) drop-shadow(0 0 3px rgba(255,196,64,.5))}
.gr2 .tx{flex:1;min-width:0}
.gr2 .hd{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.gr2 .nm{font-family:Anton;font-size:46px;line-height:1.04;color:#f3f3f3}
.gr2 .cp{font-weight:700;font-size:18px;letter-spacing:2px;color:#111;background:var(--y);padding:3px 9px}
.gr2 p{font-weight:600;font-size:29px;line-height:1.24;color:#dcdcdc;margin-top:8px}
.gr2.c4{padding:10px 22px 10px 8px}.gr2.c4 .gw{width:440px;height:160px}.gr2.c4 .gw img{max-width:432px;max-height:154px}.gr2.c4 .nm{font-size:40px}.gr2.c4 p{font-size:26px}
"""


def guns(s, d):
    """Weapon-render rows (official camo renders, cut out, fine gold edge glow) + name, chip, requirement."""
    tag = f'<div class="mtag {s.get("tag_cls", "tech")}" style="top:252px">{E(s["tag"])}</div>' if s.get('tag') else ''
    c4 = ' c4' if len(s['guns']) >= 4 else ''
    rows = ''.join(f'<div class="pc hud gr2{c4}"><div class="gw"><img src="/_build/s1/{g["img"]}"></div><div class="tx"><div class="hd"><span class="nm">{E(g["name"].upper())}</span>'
                   + (f'<span class="cp">{E(g["chip"])}</span>' if g.get('chip') else '') + f'</div><p>{E(g["desc"])}</p></div></div>' for g in s['guns'])
    body = (f'<div class="sec">{E(s["sec"])}</div><div class="fit" style="top:235px" data-size="120" data-max="{s.get("title_max", 700)}"><span class="gr w">{E(s["title"])}</span></div>'
            + tag + f'<div class="stack" style="top:385px;gap:18px">{rows}</div>'
            + (f'<div class="s1ft" style="top:1250px">{E(s["foot"])}</div>' if s.get('foot') else ''))
    return page(body, {**d, 'footer': ''})


def bleed(img, top):
    """Screenshot full-bleed across the whole 1080 width, COMPLETE (no crop, own aspect ratio)."""
    from PIL import Image
    iw, ih = Image.open(os.path.join(R.HERE, '_build', 's1', img)).size
    h = round(1080 * ih / iw)
    return f'<div class="bleed" style="top:{top}px;height:{h}px;background-image:url(/_build/s1/{img})"></div>', h


def shot(s, d):
    """Graphics showcase slide: section line, big title + status tag (NEW S1 / LAUNCH MAP), full-bleed screenshot, 2 caption lines."""
    tag = f'<div class="mtag {s.get("tag_cls", "old")}" style="top:252px">{E(s["tag"])}</div>' if s.get('tag') else ''
    bb, h = bleed(s['shot'], 400)
    cap = ''.join(f'<div class="ln"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in s['rules'])
    body = (f'<div class="sec">{E(s["sec"])}</div><div class="fit" style="top:235px" data-size="120" data-max="700"><span class="gr w">{E(s["title"])}</span></div>'
            + tag + bb + f'<div class="shotcap" style="top:{400 + h + 44}px">{cap}</div>')
    return page(body, {**d, 'footer': ''})


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


def settings(rs):
    return ''.join(f'<div class="pc hud st"><div class="l"><b>{E(r[0])}</b>' + (f'<p>{E(r[2])}</p>' if len(r) > 2 and r[2] else '')
                   + f'</div><div class="v">{E(r[1])}</div></div>' for r in rs)


def rules(rs):
    return ''.join(f'<div class="pc hud ru"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in rs)


def slide(s, d):
    if s.get('shot'):
        return shot(s, d)
    if s.get('guns'):
        return guns(s, d)
    head = f'<div class="sec">{E(s["sec"])}</div><div class="fit" style="top:240px" data-size="100" data-max="860"><span class="gr w">{E(s["title"])}</span></div>'
    if s.get('hero'):
        hw = s.get('hero_w', 885); hh, h = hero(s['hero'], 365, s.get('hero_max', 470), maxw=hw, left=(1080 - hw) // 2 if hw > 885 else 50)
        body = head + hh + f'<div class="stack" style="top:{365 + h + 22}px;gap:10px">{rules(s["rules"])}</div>'
    else:
        inner = ''.join(card(c, len(s.get('cards', [])) >= 5) for c in s.get('cards', [])) + (rules(s['rules']) if s.get('rules') else '') + (settings(s['settings']) if s.get('settings') else '')
        body = head + f'<div class="stack" style="top:365px;gap:16px">{inner}</div>'
        if s.get('foot'):
            body += f'<div class="s1ft" style="top:1230px">{E(s["foot"])}</div>'
    return page(body, {**d, 'footer': ''})


def cover_rows(c):
    """Cover variant without photo: one weapon render (gold edge glow) + numbered HUD rows (label + teaser)."""
    gun = (f'<div class="gunbox" style="top:620px;height:270px;width:900px"><div style="display:inline-block;transform:rotate(-4deg);filter:drop-shadow(0 40px 30px rgba(0,0,0,.85))">'
           f'<img style="display:block;max-height:250px;max-width:820px;filter:drop-shadow(0 0 1px rgba(255,226,150,.95)) drop-shadow(0 0 3px rgba(255,196,64,.5)) brightness(1.2) contrast(1.08)" src="/weapons/{c["gun"]}"></div></div>'
           '<div class="floor" style="top:880px"></div><div class="line" style="top:897px"></div>') if c.get('gun') else ''
    rows = ''.join(f'<div class="row hud" style="top:{915 + i * 76}px;height:66px"><div class="n" style="font-size:44px">{i + 1:02d}</div>'
                   f'<b style="font-size:30px">{E(a)}</b><small>{E(b)}</small></div>' for i, (a, b) in enumerate(c['rows']))
    return gun + rows


def cover(d):
    c = d['cover']
    if c.get('bleed'):
        return cover_bleed(d)
    chips = ''.join(f'<span class="hud">{E(x)}</span>' for x in c.get('chips', []))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="190" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:450px" data-size="120" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:590px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + (cover_rows(c) if c.get('rows') else hero(c['img'], 650, 420)[0]
               + f'<div class="cv2"><div class="ch2" style="top:1095px">{chips}</div></div>')
            + f'<div class="swipe" style="top:1235px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': '', 'cover_logo': 1})


def cover_bleed(d):
    """Catchy cover: full-bleed screenshot, free-standing operator cut-out BEHIND the title, hook line."""
    c = d['cover']
    bb, h = bleed(c['bleed'], c.get('bleed_top', 610))
    body = (bb + (R.cutout_html(c['cutout']) if c.get('cutout') else '')
            + f'<div class="kicker" style="top:200px;left:60px;font-size:28px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="190" data-max="960"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:445px" data-size="125" data-max="700"><span class="gr w">{E(c["small"])}</span></div>'
            + (f'<div class="mtag tech" style="top:{c.get("bleed_top", 610) + h - 70}px;left:50px;right:auto">{E(c["stamp"])}</div>' if c.get('stamp') else '')
            + f'<div class="swipe" style="top:{c.get("bleed_top", 610) + h + 30}px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return page(body, {**d, 'footer': '', 'cover_logo': 1})


def cta(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:230px" data-size="130" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:375px" data-size="130" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:540px;left:60px;font-size:24px;letter-spacing:5px;color:#d9d9d9">{E(c["sub"])}</div>'
            + f'<div class="t hud save" style="position:absolute;left:150px;width:640px;top:680px;height:130px;justify-content:center"><div class="tx" style="text-align:center;padding:0"><small style="font-size:20px">{E(c.get("save_kicker","YOUR SEASON 1 CHEAT SHEET"))}</small><b style="font-size:60px">SAVE THIS</b></div></div>'
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
