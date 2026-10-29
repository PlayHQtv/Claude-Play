"""PlayHQ META carousel generator (design v3 "digital HUD", approved 29.10.2026).
Usage: python3 render.py data/<file>.json [out_dir]
Slides: cover, one per weapon, cta. 1080x1920 JPG. All components are free (OFL fonts, own textures/icons, ISNet cutouts)."""
import json, os, sys, html, threading, functools, http.server, socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape

CSS = """
@font-face{font-family:Anton;src:url(/assets/fonts/Anton-Regular.ttf)}
@font-face{font-family:Raj;src:url(/assets/fonts/Rajdhani-Bold.ttf);font-weight:700}
@font-face{font-family:Raj;src:url(/assets/fonts/Rajdhani-SemiBold.ttf);font-weight:600}
@font-face{font-family:Raj;src:url(/assets/fonts/Rajdhani-Medium.ttf);font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
:root{--y:#ffd400;--g1:#fff3c4;--g2:#e9c062;--g3:#a8761c}
body{width:1080px;height:1920px;overflow:hidden;background:#070707;font-family:Raj;color:#fff;position:relative}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse 620px 360px at 560px 1010px,rgba(255,200,60,.22),transparent 70%),radial-gradient(ellipse 900px 700px at 900px 200px,rgba(255,212,0,.07),transparent 70%),linear-gradient(180deg,#0d0d0c 0%,#080807 55%,#050505 100%)}
.topo{position:absolute;inset:0;background:url(/assets/topo.png)}
.streak{position:absolute;width:1600px;height:2px;background:linear-gradient(90deg,transparent,rgba(255,212,0,.45),transparent);transform:rotate(-32deg)}
.vign{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 50%,rgba(0,0,0,.6) 100%)}
.corner{position:absolute;width:80px;height:80px;border-color:rgba(255,212,0,.8);border-style:solid}
.top{position:absolute;left:70px;top:150px;display:flex;align-items:center;gap:18px}
.cod{font-family:Anton;font-size:44px;letter-spacing:1px;color:#f3f3f3}
.dmz{font-family:Anton;font-size:38px;color:var(--y);padding:0 16px;line-height:54px;border:1px solid rgba(255,212,0,.6);background:linear-gradient(135deg,rgba(255,212,0,.18),rgba(255,212,0,.04))}
.logo{position:absolute;right:70px;top:110px;width:160px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}
.gr{display:inline-block;-webkit-mask-image:url(/assets/grunge.png);-webkit-mask-size:1400px 700px}
.w{color:#ededed}
.gold{background:linear-gradient(170deg,var(--g1) 0%,var(--g2) 35%,var(--g3) 60%,#f5d27a 80%,var(--g2) 100%);-webkit-background-clip:text;color:transparent;-webkit-mask-position:400px 120px}
.fit{position:absolute;left:62px;font-family:Anton;line-height:1;letter-spacing:4px;white-space:nowrap}
.hud{background:linear-gradient(180deg,rgba(18,17,12,.92),rgba(8,8,7,.92));border:1px solid rgba(255,212,0,.28);position:relative;clip-path:polygon(0 0,calc(100% - 22px) 0,100% 22px,100% 100%,22px 100%,0 calc(100% - 22px))}
.hud::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 1px,transparent 1px 4px);pointer-events:none}
.hud::after{content:"";position:absolute;left:0;top:0;width:34px;height:3px;background:var(--y);box-shadow:0 0 10px rgba(255,212,0,.7)}
.foot{position:absolute;left:0;right:0;top:1836px;text-align:center;font-weight:700;font-size:24px;letter-spacing:8px;color:#9a9a9a}
.foot b{color:var(--y)}
.sub{position:absolute;left:70px;font-weight:700;font-size:54px;letter-spacing:15px;color:#f2f2f2;white-space:nowrap}
.cls{position:absolute;left:70px;font-size:38px;font-weight:600;letter-spacing:2px;display:flex;align-items:center;gap:14px;color:#cfcfcf}
.cls i{display:block;width:44px;height:5px;background:var(--y)}
.cls b{color:var(--y);font-weight:700}
.rank{position:absolute;right:70px;top:640px;text-align:right}
.rank small{display:block;font-size:24px;letter-spacing:6px;color:#bdbdbd;font-weight:700}
.rank strong{font-family:Anton;font-size:96px;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.gunbox{position:absolute;left:30px;width:1020px;display:grid;place-items:center}
.gun{max-width:1000px;transform:rotate(-4deg);filter:drop-shadow(0 40px 30px rgba(0,0,0,.85)) drop-shadow(0 0 2px rgba(255,220,140,.35))}
.floor{position:absolute;left:190px;width:700px;height:40px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,212,0,.35),transparent 70%);filter:blur(6px)}
.line{position:absolute;left:150px;width:780px;height:2px;background:linear-gradient(90deg,transparent,rgba(255,212,0,.7),transparent)}
.hdr{position:absolute;left:60px;right:60px;top:1288px;height:84px;display:flex;align-items:center;padding:0 30px}
.hdr span{font-weight:700;font-size:36px;letter-spacing:12px}
.ticks{margin-left:auto;display:flex;align-items:center;gap:18px}
.ticks i{display:block;width:120px;height:10px;background:repeating-linear-gradient(90deg,rgba(255,212,0,.6) 0 2px,transparent 2px 10px)}
.ticks em{font-style:normal;font-size:23px;letter-spacing:6px;color:var(--y);font-weight:700}
.grid{position:absolute;left:60px;right:60px;top:1392px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.t{height:124px;display:flex;align-items:center;gap:18px;padding:0 16px}
.ic{width:156px;height:94px;flex:none;position:relative;display:grid;place-items:center;background:linear-gradient(rgba(255,212,0,.06) 1px,transparent 1px) 0 0/12px 12px,linear-gradient(90deg,rgba(255,212,0,.06) 1px,transparent 1px) 0 0/12px 12px,radial-gradient(ellipse at 50% 50%,rgba(255,212,0,.10),rgba(0,0,0,0) 70%);border:1px solid rgba(255,212,0,.18)}
.ic::before,.ic::after{content:"";position:absolute;width:12px;height:12px;border-color:var(--y);border-style:solid}
.ic::before{left:-1px;top:-1px;border-width:2px 0 0 2px}.ic::after{right:-1px;bottom:-1px;border-width:0 2px 2px 0}
.ic img{width:146px}
.num{position:absolute;right:16px;top:10px;font-size:18px;font-weight:700;letter-spacing:3px;color:rgba(255,212,0,.45)}
.tx b{display:block;white-space:nowrap;font-weight:700;font-size:32px;color:#fff;letter-spacing:1px;line-height:1.05}
.tx small{display:block;font-weight:700;font-size:21px;color:var(--y);letter-spacing:5px;margin-top:6px}
.save{background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);border:none}
.save::after{background:#111;box-shadow:none}
.save .tx{padding-left:14px}
.save .tx b{color:#140f00;font-family:Anton;font-size:46px;font-weight:400;letter-spacing:1px}
.save .tx small{color:#3a2a00;letter-spacing:5px;font-size:21px;margin:0 0 2px}
.kicker{position:absolute;left:70px;font-weight:700;font-size:34px;letter-spacing:14px;color:var(--y)}
.card{position:absolute;width:465px;height:258px}
.card .badge{position:absolute;left:18px;top:18px;font-family:Anton;font-size:44px;line-height:60px;width:60px;text-align:center;color:#140f00;background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);clip-path:polygon(0 0,100% 0,100% 70%,70% 100%,0 100%)}
.card .cimg{position:absolute;left:20px;right:20px;top:56px;height:128px;display:grid;place-items:center}
.card .cimg img{max-width:370px;max-height:120px;filter:drop-shadow(0 16px 12px rgba(0,0,0,.8))}
.card .nm{position:absolute;left:24px;bottom:22px;font-weight:700;font-size:34px;letter-spacing:3px}
.card .cl{position:absolute;right:24px;bottom:28px;font-weight:700;font-size:20px;letter-spacing:4px;color:var(--y)}
.swipe{position:absolute;left:0;right:0;text-align:center;font-weight:700;font-size:34px;letter-spacing:12px;color:var(--y)}
.row{position:absolute;left:60px;right:60px;height:118px;display:flex;align-items:center;gap:24px;padding:0 26px}
.row .n{font-family:Anton;font-size:56px;width:70px;text-align:center;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.row img{width:230px;max-height:96px;object-fit:contain;filter:drop-shadow(0 10px 8px rgba(0,0,0,.8))}
.row b{font-weight:700;font-size:40px;letter-spacing:3px}
.row small{margin-left:auto;font-weight:700;font-size:22px;letter-spacing:5px;color:var(--y)}
"""

FRAME = """<div class="bg"></div><div class="topo"></div>
<div class="streak" style="left:-300px;top:560px"></div><div class="streak" style="left:200px;top:1260px;opacity:.6"></div>
<div class="vign"></div>
<div class="corner" style="left:28px;top:28px;border-width:3px 0 0 3px"></div><div class="corner" style="right:28px;top:28px;border-width:3px 3px 0 0"></div>
<div class="corner" style="left:28px;bottom:28px;border-width:0 0 3px 3px"></div><div class="corner" style="right:28px;bottom:28px;border-width:0 3px 3px 0"></div>
<div class="top"><div class="cod">{game}</div><div class="dmz">{badge}</div></div>
<img class="logo" src="/assets/logo.png">"""

# Auto-fit: shrink every .fit element until it is <= data-max px wide.
FITJS = """<script>document.fonts.ready.then(()=>{for(const e of document.querySelectorAll('.fit,.shrink')){let s=+e.dataset.size;e.style.fontSize=s+'px';while(e.scrollWidth>+e.dataset.max&&s>16){s-=2;e.style.fontSize=s+'px'}if(e.dataset.zone){const[t,h]=e.dataset.zone.split(',').map(Number);e.style.top=(t+(h-s)/2)+'px'}}document.body.dataset.ready=1})</script>"""


def page(body, d):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            + FRAME.format(game=E(d.get('game', 'CALL OF DUTY · MW4')), badge=E(d.get('badge', 'DMZ'))) + body
            + f'<div class="foot">{d.get("footer", "FOLLOW <b>@PLAYHQTV</b> FOR DAILY MW4 META")}</div>' + FITJS + '</body></html>')


def title_html(white, gold, top, size=250, max_w=950):
    """One line if it fits at >=200px, otherwise white on line 1 and gold on line 2."""
    if len(white) + len(gold) <= 10:
        return (f'<div class="fit" style="top:{top}px" data-size="{size}" data-max="{max_w}" data-zone="{top},{size + 10}">'
                f'<span class="gr w">{E(white)}</span><span class="gr gold" style="margin-left:28px">{E(gold)}</span></div>')
    h = size // 2
    return (f'<div class="fit" style="top:{top}px" data-size="{h}" data-max="{max_w}"><span class="gr w">{E(white)}</span></div>'
            f'<div class="fit" style="top:{top + h + 6}px" data-size="{h}" data-max="{max_w}"><span class="gr gold">{E(gold)}</span></div>')


def weapon_slide(w, d):
    tiles = ''.join(
        f'<div class="t hud"><span class="num">{i + 1:02d}</span><div class="ic"><img src="/assets/icons/{a["type"]}.svg"></div>'
        + (f'<div class="tx"><b class="shrink" data-size="32" data-max="262">{E(a["name"])}</b>' if len(a["name"]) <= 16 else f'<div class="tx"><b style="font-size:27px;white-space:normal;max-width:236px;line-height:1.08">{E(a["name"])}</b>')
        + f'<small>{E(a["label"])}</small></div></div>'
        for i, a in enumerate(w['attachments'][:5]))
    if w.get('apex'):
        tiles += (f'<div class="t hud save"><div class="ic" style="background:rgba(0,0,0,.18);border-color:rgba(0,0,0,.35)"><img src="/assets/icons/apex.svg" style="filter:brightness(.25)"></div>'
                  f'<div class="tx" style="padding-left:0"><small>APEX</small><b class="shrink" data-size="44" data-max="250">{E(w["apex"])}</b></div></div>')
    else:
        tiles += '<div class="t hud save"><div class="tx"><small>DON\'T LOSE IT</small><b>SAVE THIS BUILD</b></div></div>'
    br = w.get('brightness', 1.18)
    body = (title_html(w['title_white'], w['title_gold'], 300)
            + f'<div class="fit sub" style="top:635px;left:70px;font-family:Raj;letter-spacing:15px" data-size="54" data-max="700">{E(w.get("tagline", "EXTRACTION READY"))}</div>'
            + f'<div class="cls" style="top:712px"><i></i>{E(w["class"])} — <b>{E(w.get("class_note", "Meta Loadout"))}</b></div>'
            + f'<div class="rank"><small>{E(d.get("rank_label", "META RANK"))}</small><strong>#{w["rank"]}</strong></div>'
            + '<div class="floor" style="top:1205px"></div><div class="line" style="top:1222px"></div>'
            + f'<div class="gunbox" style="top:800px;height:420px"><img class="gun" style="max-height:400px;filter:drop-shadow(0 40px 30px rgba(0,0,0,.85)) drop-shadow(0 0 2px rgba(255,220,140,.35)) brightness({br}) contrast(1.08)" src="/weapons/{w["image"]}"></div>'
            + f'<div class="hdr hud"><span>ATTACHMENTS</span><div class="ticks"><i style="width:60px"></i><div style="text-align:right;line-height:1.1"><small style="display:block;font-size:17px;letter-spacing:5px;color:#bdbdbd;font-weight:700">BUILD CODE</small><em>{E(w.get("build_code", ""))}</em></div></div></div>'
            + f'<div class="grid">{tiles}</div>')
    return page(body, d)


def cover_slide(d):
    c = d['cover']
    pos = [(60, 725), (555, 725), (60, 997), (555, 997)]
    cards = ''.join(
        f'<div class="card hud" style="left:{x}px;top:{y}px"><div class="badge">{w["rank"]}</div>'
        f'<div class="cimg"><img src="/weapons/{w["image"]}" style="filter:drop-shadow(0 16px 12px rgba(0,0,0,.8)) brightness({w.get("brightness", 1.18)})"></div>'
        f'<div class="nm">{E(w["short"])}</div><div class="cl">{E(w["class"].upper())}</div></div>'
        for (x, y), w in zip(pos, d['weapons']))
    body = (f'<div class="kicker" style="top:300px">{E(c.get("kicker", "UPDATED"))}</div>'
            + f'<div class="fit" style="top:345px" data-size="250" data-max="950"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:590px" data-size="120" data-max="950"><span class="gr w">{E(c["small"])}</span></div>'
            + cards + f'<div class="swipe" style="top:1292px">{E(c.get("swipe", "SWIPE FOR THE LOADOUTS ›"))}</div>')
    return page(body, d)


def cta_slide(d):
    c = d['cta']
    rows = ''.join(
        f'<div class="row hud" style="top:{860 + i * 134}px"><div class="n">{w["rank"]}</div><img src="/weapons/{w["image"]}" style="filter:drop-shadow(0 10px 8px rgba(0,0,0,.8)) brightness({w.get("brightness", 1.18)})">'
        f'<b>{E(w["short"])}</b><small>{E(w["class"].upper())}</small></div>' for i, w in enumerate(d['weapons']))
    body = (f'<div class="fit" style="top:330px" data-size="180" data-max="950"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:530px" data-size="180" data-max="950"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:760px;letter-spacing:10px;color:#d9d9d9">{E(c.get("sub", "DROP THE NUMBER IN THE COMMENTS"))}</div>'
            + rows
            + '<img src="/assets/logo.png" style="position:absolute;left:440px;top:1420px;width:200px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.7))">'
            + '<div style="position:absolute;left:0;right:0;top:1640px;text-align:center;font-family:Anton;font-size:84px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
            + f'<div class="swipe" style="top:1745px;color:#cfcfcf;letter-spacing:10px;font-size:30px">{E(c.get("follow_sub", "FOR DAILY MW4 META"))}</div>')
    return page(body, {**d, 'footer': ''})


def serve(root):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    h.log_message = lambda *a: None
    s = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    out_dir = out_dir or os.path.join(HERE, 'out', os.path.splitext(os.path.basename(data_path))[0])
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    pages = [('01_cover', cover_slide(d))]
    for i, w in enumerate(d['weapons']):
        pages.append((f'{i + 2:02d}_{w["image"].split(".")[0]}', weapon_slide(w, d)))
    pages.append((f'{len(pages) + 1:02d}_cta', cta_slide(d)))
    srv = serve(HERE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for name, h in pages:
            open(os.path.join(tmp, name + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{name}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out_dir, name + '.jpg'), type='jpeg', quality=92)
            print(os.path.join(out_dir, name + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
