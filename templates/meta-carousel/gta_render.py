"""PlayHQ GTA VI carousel design ("Vice" style): sunset gradients, neon accents, glass cards.
Usage: python3 gta_render.py data/<file>.json <out_dir>. Images come from _build/gta/ (private, never committed):
official logo (logo_gta6.png), official character art (cut_*.png) and official screenshots."""
import json, os, sys
import render as R

E = R.E
CSS = """
@font-face{font-family:Bebas;src:url(/assets/fonts/BebasNeue.woff2)}
@font-face{font-family:Tail;src:url(/assets/fonts/Yellowtail.woff2)}
@font-face{font-family:In;src:url(/assets/fonts/Inter-600.woff2);font-weight:600}
@font-face{font-family:In;src:url(/assets/fonts/Inter-700.woff2);font-weight:700}
@font-face{font-family:In;src:url(/assets/fonts/Inter-800.woff2);font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
:root{--p:#ff4fa3;--o:#ffb04a;--v:#8a4dff;--t:#36e6d4;--ink:#0f0717}
html,body{width:1080px;height:1440px;overflow:hidden}
body{position:relative;background:var(--ink);color:#fff;font-family:In}
.sky{position:absolute;inset:0;background:
 radial-gradient(1200px 700px at 85% -10%,rgba(255,79,163,.55),transparent 60%),
 radial-gradient(900px 600px at 0% 105%,rgba(54,230,212,.22),transparent 60%),
 linear-gradient(180deg,#2a0f3d 0%,#170a24 45%,#0f0717 100%)}
.bgimg{position:absolute;inset:0;background-size:cover;background-position:center}
.duo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,8,44,.78) 0%,rgba(60,14,70,.55) 35%,rgba(255,79,163,.22) 62%,rgba(15,7,23,.92) 100%)}
.sun{position:absolute;border-radius:50%;background:linear-gradient(180deg,#ffd36b 0%,#ff9a4a 40%,#ff4fa3 75%,#c23bd6 100%);
 -webkit-mask-image:repeating-linear-gradient(180deg,#000 0,#000 20px,transparent 20px,transparent 30px),linear-gradient(#000 45%,transparent 46%);
 -webkit-mask-composite:source-over;mask-composite:add;filter:drop-shadow(0 0 60px rgba(255,79,163,.55))}
.sunwrap{position:absolute;opacity:.85}
.sunwrap::after{content:"";position:absolute;inset:0;border-radius:50%;background:linear-gradient(180deg,#ffd36b,#ff4fa3);-webkit-mask-image:linear-gradient(#000 0 44%,transparent 44.5%)}
.palm{position:absolute;filter:drop-shadow(0 0 30px rgba(255,79,163,.25))}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,214,240,.16) 1.3px,transparent 1.8px);background-size:14px 14px;-webkit-mask-image:linear-gradient(180deg,#000 0,transparent 55%)}
.grain{position:absolute;inset:0;background:url(/assets/grain.png);mix-blend-mode:overlay;opacity:.16}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 220px rgba(0,0,0,.75)}
.grid{position:absolute;left:0;right:0;bottom:0;height:420px;opacity:.22;
 background:linear-gradient(transparent 0,transparent 47px,rgba(255,79,163,.7) 48px),linear-gradient(90deg,transparent 0,transparent 89px,rgba(255,79,163,.5) 90px);
 background-size:100% 48px,90px 100%;-webkit-mask-image:linear-gradient(transparent,#000 70%);transform:perspective(600px) rotateX(55deg);transform-origin:bottom}
.hdr{position:absolute;left:56px;top:128px;display:flex;align-items:center;gap:16px}
.hdr .chip{font-family:Bebas;font-size:40px;letter-spacing:2px;padding:4px 14px 0;background:linear-gradient(90deg,var(--p),var(--o));color:#170a24;border-radius:8px;line-height:1.1}
.hdr .tx{font-family:Bebas;font-size:40px;letter-spacing:3px;color:#ffe9f4}
.glogo{position:absolute;left:52px;top:112px;height:140px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.6))}
.plogo{position:absolute;right:170px;top:118px;width:92px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}
.kick{position:absolute;left:56px;font-family:Bebas;font-size:34px;letter-spacing:5px;color:#12061c;background:var(--t);padding:5px 16px 1px;transform:rotate(-2deg);box-shadow:5px 5px 0 #12061c;white-space:nowrap}
.ttl{position:absolute;left:52px;white-space:nowrap;font-family:Bebas;line-height:.88;letter-spacing:1px;
 background:linear-gradient(180deg,#fff3c9 0%,var(--o) 38%,var(--p) 78%,var(--v) 100%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(3px 0 0 #12061c) drop-shadow(-3px 0 0 #12061c) drop-shadow(0 3px 0 #12061c) drop-shadow(0 -3px 0 #12061c) drop-shadow(0 9px 0 #12061c) drop-shadow(0 22px 30px rgba(0,0,0,.55))}
.ttl.w{background:linear-gradient(180deg,#fff,#ffe1f0);-webkit-background-clip:text}
.scr{position:absolute;left:62px;font-family:Tail;color:#fff;text-shadow:0 0 6px var(--p),0 0 22px var(--p),0 0 44px rgba(255,79,163,.7);transform:rotate(-4deg);white-space:nowrap}
.photo{position:absolute;left:0;width:1080px;background-size:cover;background-position:center}
.photo.fade{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 18%,#000 72%,transparent 100%)}
.shot{position:absolute;left:40px;width:1000px;border-radius:26px;background-size:100% 100%;box-shadow:0 30px 60px rgba(0,0,0,.6),0 0 0 3px rgba(255,255,255,.08)}
.shot::after{content:"";position:absolute;inset:0;border-radius:26px;box-shadow:inset 0 0 0 3px rgba(255,79,163,.55)}
.tag{position:absolute;right:56px;font-family:Bebas;font-size:36px;letter-spacing:2px;padding:6px 18px 2px;border-radius:999px;color:#170a24;background:var(--t)}
.cards{position:absolute;left:56px;width:880px;display:flex;flex-direction:column;gap:18px}
.card{display:flex;gap:22px;align-items:center;padding:22px 26px;border-radius:24px;background:linear-gradient(135deg,rgba(40,14,58,.86),rgba(18,6,28,.82));
 box-shadow:inset 0 0 0 2px rgba(255,255,255,.10),0 20px 40px rgba(0,0,0,.35);backdrop-filter:blur(6px);position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:linear-gradient(180deg,var(--o),var(--p),var(--v))}
.card .n{flex:none;width:86px;height:86px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Bebas;font-size:58px;color:#170a24;background:linear-gradient(135deg,var(--o),var(--p));padding-top:6px}
.card b{display:block;font-family:Bebas;font-size:54px;line-height:1;letter-spacing:1px;color:#fff}
.card p{font-weight:600;font-size:28px;line-height:1.28;color:#f1dceb;margin-top:6px}
.card p em{font-style:normal;color:var(--t);font-weight:700}
.cap{position:absolute;left:56px;width:880px}
.cap .ln{display:flex;gap:20px;align-items:baseline;margin-bottom:20px}
.cap .ln b{flex:none;width:310px;font-family:Bebas;font-size:50px;line-height:1;background:linear-gradient(90deg,var(--o),var(--p));-webkit-background-clip:text;color:transparent}
.cap .ln p{flex:1;font-weight:600;font-size:33px;line-height:1.28;color:#f4e6ef}
.swipe{position:absolute;right:120px;font-family:Bebas;font-size:40px;letter-spacing:4px;color:#fff;text-shadow:0 0 16px rgba(255,79,163,.8)}
.src{position:absolute;left:56px;right:140px;bottom:96px;font-weight:600;font-size:20px;letter-spacing:1px;color:rgba(255,233,244,.65)}
.cut{position:absolute;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6));-webkit-mask-image:linear-gradient(180deg,#000 80%,transparent 99%)}
.panel{position:absolute;background-size:100% 100%;border:10px solid #fff;box-shadow:10px 12px 0 #12061c,0 30px 50px rgba(0,0,0,.5)}
.panel span{position:absolute;left:-10px;top:-10px;font-family:Bebas;font-size:34px;letter-spacing:3px;background:#12061c;color:#fff;padding:6px 14px 2px}
.foot{position:absolute;left:0;right:0;bottom:52px;text-align:center;font-family:Bebas;font-size:30px;letter-spacing:6px;color:rgba(255,233,244,.8)}
.foot b{color:var(--p);font-weight:400}
"""


def page(body, d, cover=False):
    head = (f'<img class="glogo" src="/_build/gta/logo_gta6.png">' if cover else
            f'<div class="hdr"><span class="chip">GTA 6</span><span class="tx">{E(d.get("hdr", "TIPS & TRICKS"))}</span></div>')
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>'
            '<div class="sky"></div>'
            + (f'<div class="bgimg" style="background-image:url(/_build/gta/{d["bg"]})"></div><div class="duo"></div>' if d.get('bg') else '')
            + f'<div class="sunwrap" style="{d.get("sun", "right:-120px;top:150px")};width:{d.get("sun_d", 520)}px;height:{d.get("sun_d", 520)}px"><div class="sun" style="position:absolute;inset:0"></div></div>'
            + '<div class="dots"></div><div class="grid"></div>'
            + ('' if d.get('no_palms') else '<img class="palm" src="/assets/palm.svg" style="left:-170px;bottom:-60px;height:820px;transform:scaleX(-1)"><img class="palm" src="/assets/palm.svg" style="right:-210px;bottom:-40px;height:660px">')
            + '<div class="vig"></div><div class="grain"></div>' + body + head
            + '<img class="plogo" src="/assets/logo.png">'
            + (f'<div class="src">{E(d["source"])}</div>' if d.get('source') else '')
            + '<div class="foot">FOLLOW <b>@PLAYHQTV</b> FOR GTA 6 TIPS</div>' + R.FITJS + '</body></html>')


def cover(d):
    """GTA box-art style: tilted official screenshot panels with white frames, official character art in front, outlined title."""
    c = d['cover']
    cut = c.get('cutout')
    panels = ''.join(f'<div class="panel" style="left:{p["x"]}px;top:{p["y"]}px;width:{p["w"]}px;height:{round(p["w"] * 9 / 16)}px;transform:rotate({p.get("r", 0)}deg);background-image:url(/_build/gta/{p["img"]})">'
                     + (f'<span>{E(p["label"])}</span>' if p.get('label') else '') + '</div>' for p in c.get('panels', []))
    body = (panels
            + (f'<img class="cut" src="/_build/gta/{cut["img"]}" style="right:{cut.get("right", -40)}px;top:{cut.get("top", 300)}px;height:{cut.get("h", 1100)}px">' if cut else '')
            + f'<div class="kick" style="top:282px">{E(c["kicker"])}</div>'
            + f'<div class="ttl fit" style="top:338px" data-size="190" data-max="{c.get("max", 980)}">{E(c["big"])}</div>'
            + f'<div class="scr fit" style="top:{c.get("script_top", 490)}px" data-size="120" data-max="760">{E(c["script"])}</div>'
            + f'<div class="swipe" style="top:1278px;left:58px;right:auto">{E(c["swipe"])}</div>')
    return page(body, {**d, 'source': '', 'bg': c.get('bg', d.get('bg')), 'sun': c.get('sun', 'right:-60px;top:330px'), 'sun_d': c.get('sun_d', 560)}, cover=True)


def shot(s, d):
    d = {**d, 'bg': s.get('bg', d.get('bg'))}
    from PIL import Image
    iw, ih = Image.open(os.path.join(R.HERE, '_build', 'gta', s['shot'])).size
    h = round(1000 * ih / iw)
    cap = ''.join(f'<div class="ln"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in s['rules'])
    body = (f'<div class="kick" style="top:222px">{E(s["kicker"])}</div>'
            + f'<div class="ttl w fit" style="top:262px" data-size="150" data-max="{700 if s.get("tag") else 960}">{E(s["title"])}</div>'
            + (f'<div class="tag" style="top:292px">{E(s["tag"])}</div>' if s.get('tag') else '')
            + f'<div class="shot" style="top:430px;height:{h}px;background-image:url(/_build/gta/{s["shot"]})"></div>'
            + f'<div class="cap" style="top:{430 + h + 50}px">{cap}</div>')
    return page(body, d)


def cards(s, d):
    d = {**d, 'bg': s.get('bg', d.get('bg'))}
    cs = ''.join(f'<div class="card"><div class="n">{i + 1}</div><div><b>{E(a)}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(s['cards']))
    body = (f'<div class="kick" style="top:222px">{E(s["kicker"])}</div>'
            + f'<div class="ttl w fit" style="top:262px" data-size="150" data-max="960">{E(s["title"])}</div>'
            + f'<div class="cards" style="top:430px">{cs}</div>')
    return page(body, d)


def cta(d):
    c = d['cta']
    d = {**d, 'bg': c.get('bg', d.get('bg')), 'sun': 'left:-140px;top:820px'}
    cut = c.get('cutout')
    body = ((f'<img class="cut" src="/_build/gta/{cut["img"]}" style="right:{cut.get("right", -60)}px;top:{cut.get("top", 560)}px;height:{cut.get("h", 860)}px;opacity:.95">' if cut else '')
            + f'<div class="ttl w fit" style="top:262px" data-size="150" data-max="960">{E(c["white"])}</div>'
            + f'<div class="ttl fit" style="top:397px" data-size="150" data-max="960">{E(c["gold"])}</div>'
            + f'<div class="scr fit" style="top:560px" data-size="96" data-max="560">{E(c["script"])}</div>'
            + '<div style="position:absolute;left:56px;top:760px;width:520px;padding:26px 30px;border-radius:24px;background:linear-gradient(135deg,var(--o),var(--p));color:#170a24">'
              '<div style="font-family:Bebas;font-size:30px;letter-spacing:4px">YOUR GTA 6 CHEAT SHEET</div><div style="font-family:Bebas;font-size:78px;line-height:1">SAVE THIS</div></div>'
            + '<div style="position:absolute;left:56px;top:1000px;font-family:Bebas;font-size:66px;letter-spacing:2px;background:#12061c;padding:12px 24px 4px;box-shadow:7px 7px 0 var(--p);transform:rotate(-2deg)">FOLLOW <span style="color:var(--o)">@PLAYHQTV</span></div>')
    return page(body, {**d, 'source': ''})


def slide(s, d):
    return shot(s, d) if s.get('shot') else cards(s, d)


def main(data_path, out_dir):
    d = json.load(open(data_path))
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover(d))] + [(f'{i + 2:02d}_slide', slide(s, d)) for i, s in enumerate(d['slides'])]
    pages.append((f'{len(pages) + 1:02d}_cta', cta(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=3)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(500)
            raw = os.path.join(tmp, nm + '@3x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            R.save_jpg(im, os.path.join(out_dir, nm + '.jpg')); print(os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
