"""PlayHQ 9:16 video frame for 16:9 gameplay clips.

Renders a 1080x1920 PNG with a transparent window where the 16:9 video sits
(full width, 608 px high). Hook text goes in the top band and the question
plus logo in the bottom band, so nothing covers the gameplay.

Usage: python frame.py jobs/<name>.json  ->  out/<name>.png
Job JSON: {"hook_white": "4 KILLS =", "hook_gold": "YOU'RE HUNTED",
           "kicker": "MW4 DMZ · BOUNTY SYSTEM", "question": "HUNTER OR HUNTED?",
           "sub": "COMMENT BELOW", "video_top": 640}
Cloudinary composite: video c_scale,w_1080 -> c_pad,w_1080,h_1920,b_rgb:070707,g_north,y_<video_top>
then l_<frame png>,fl_layer_apply,g_north. Simplest: c_pad,w_1080,h_1920,g_center (video_top 656 for 16:9).
"""
import json, os, sys, html, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'meta-carousel')
E = html.escape


def page(j):
    vt = int(j.get('video_top', 640))
    vb = vt + 608
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url(/assets/fonts/Anton-Regular.ttf)}}
@font-face{{font-family:Raj;src:url(/assets/fonts/Rajdhani-Bold.ttf);font-weight:700}}
:root{{--y:#ffd400;--g1:#fff3c4;--g2:#e9c062;--g3:#a8761c}}
html,body{{margin:0;background:transparent}}
body{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Raj;color:#fff}}
.band{{position:absolute;left:0;right:0;overflow:hidden;
  background:radial-gradient(ellipse 700px 260px at 540px 100%,rgba(255,200,60,.16),transparent 70%),
             linear-gradient(180deg,#0d0d0c,#070707)}}
.band.bot{{background:radial-gradient(ellipse 700px 260px at 540px 0%,rgba(255,200,60,.16),transparent 70%),
             linear-gradient(180deg,#070707,#050505)}}
.band::after{{content:"";position:absolute;inset:0;background:url(/assets/topo.png) center/cover;opacity:.10}}
.edge{{position:absolute;left:0;right:0;height:4px;background:linear-gradient(90deg,transparent,var(--g2) 20%,var(--g1) 50%,var(--g2) 80%,transparent)}}
.tick{{position:absolute;width:46px;height:46px;border:4px solid var(--y)}}
.hdr{{position:absolute;left:60px;top:200px;display:flex;align-items:center;gap:16px}}
.cod{{font-family:Anton;font-size:32px;letter-spacing:1px;color:#f3f3f3}}
.dmz{{font-family:Anton;font-size:28px;color:var(--y);padding:0 12px;line-height:40px;border:1px solid rgba(255,212,0,.6);background:rgba(255,212,0,.12)}}
.logo{{position:absolute;right:60px;top:176px;width:104px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}}
.kick{{position:absolute;left:60px;font-weight:700;font-size:34px;letter-spacing:9px;color:#cfcfcf}}
.hook{{position:absolute;left:56px;font-family:Anton;line-height:1.02;letter-spacing:2px;white-space:nowrap}}
.w{{color:#f2f2f2}}
.gold{{background:linear-gradient(170deg,var(--g1) 0%,var(--g2) 40%,var(--g3) 65%,#f5d27a 85%,var(--g2) 100%);-webkit-background-clip:text;color:transparent}}
.q{{position:absolute;left:60px;font-family:Anton;font-size:84px;line-height:1;white-space:nowrap}}
.sub{{position:absolute;left:62px;font-weight:700;font-size:32px;letter-spacing:8px;color:#bdbdbd}}
</style></head><body>
<div class="band" style="top:0;height:{vt}px"></div>
<div class="band bot" style="top:{vb}px;bottom:0"></div>
<div class="edge" style="top:{vt-4}px"></div><div class="edge" style="top:{vb}px"></div>
<div class="tick" style="left:24px;top:{vt-28}px;border-right:0;border-bottom:0"></div>
<div class="tick" style="right:24px;top:{vt-28}px;border-left:0;border-bottom:0"></div>
<div class="tick" style="left:24px;top:{vb-18}px;border-right:0;border-top:0"></div>
<div class="tick" style="right:24px;top:{vb-18}px;border-left:0;border-top:0"></div>
<div class="hdr"><span class="cod">CALL OF DUTY · MW4</span><span class="dmz">{E(j.get('badge','DMZ'))}</span></div>
<img class="logo" src="/assets/logo.png">
<div class="kick" style="top:{vt-330}px">{E(j.get('kicker',''))}</div>
<div class="hook fit" style="top:{vt-275}px" data-max="960"><span class="w" style="font-size:118px">{E(j['hook_white'])}</span><br><span class="gold" style="font-size:118px">{E(j['hook_gold'])}</span></div>
<div class="q fit" style="top:{vb+60}px" data-max="840"><span class="w">{E(j.get('question',''))}</span></div>
<div class="sub" style="top:{vb+165}px">{E(j.get('sub',''))} <span style="color:var(--y)">↓</span></div>
<script>
document.querySelectorAll('.fit').forEach(el=>{{const m=+el.dataset.max;let s=1;
 while(el.scrollWidth>m && s>0.4){{s-=0.02;el.querySelectorAll('span').forEach(sp=>{{sp.style.fontSize=(parseFloat(getComputedStyle(sp).fontSize)*0.98)+'px'}})}}}});
</script></body></html>"""


def serve(root):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    socketserver.TCPServer.allow_reuse_address = True
    s = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main(job):
    j = json.load(open(job))
    name = os.path.splitext(os.path.basename(job))[0]
    os.makedirs(os.path.join(ASSETS, '_build'), exist_ok=True)
    open(os.path.join(ASSETS, '_build', f'frame_{name}.html'), 'w').write(page(j))
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    out = os.path.join(HERE, 'out', f'{name}.png')
    srv = serve(ASSETS)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=2)
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/frame_{name}.html')
        pg.wait_for_timeout(500)
        tmp = out + '.2x.png'
        pg.screenshot(path=tmp, omit_background=True)
        b.close()
    srv.shutdown()
    Image.open(tmp).resize((1080, 1920), Image.LANCZOS).save(out, optimize=True)
    os.remove(tmp)
    print(out)


if __name__ == '__main__':
    main(sys.argv[1])
