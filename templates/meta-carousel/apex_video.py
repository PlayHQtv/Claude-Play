"""PlayHQ apex showcase video (9:16, 1080x1920, 30 fps).
Each weapon gets a 2.5D showcase: slow turn left/right, a light sweep across the metal, a float and a card that slides in.
Then a gold light-wipe transition moves to the next weapon.
Usage: python3 apex_video.py data/<file>.json "Apex A,Apex B" out.mp4
Frames are rendered deterministically with Playwright: JS draw(t), one screenshot per frame, then ffmpeg."""
import json, os, sys, subprocess, shutil
import render as R

E = R.E
FPS = 30
SEG = 5.0      # seconds per weapon
TR = 0.6       # transition length

CSS = R.CSS.replace('height:1440px', 'height:1920px') + """
.stage{position:absolute;left:0;right:0;top:560px;height:470px;perspective:1600px;display:grid;place-items:center}
.wrap{position:relative;will-change:transform}
.wrap img.g{display:block;max-width:900px;max-height:400px;filter:drop-shadow(0 40px 30px rgba(0,0,0,.85)) brightness(1.18) contrast(1.08)}
.shine{position:absolute;inset:0;-webkit-mask-size:100% 100%;-webkit-mask-repeat:no-repeat;mix-blend-mode:screen;pointer-events:none}
.shadow{position:absolute;left:50%;top:1020px;width:640px;height:46px;margin-left:-320px;border-radius:50%;
  background:radial-gradient(ellipse,rgba(255,212,0,.32),transparent 70%);filter:blur(8px)}
.ring{position:absolute;left:50%;top:1035px;width:760px;height:2px;margin-left:-380px;background:linear-gradient(90deg,transparent,rgba(255,212,0,.75),transparent)}
.vcard{position:absolute;left:50px;width:870px;top:1110px;height:330px}
.vcard .ix{position:absolute;left:36px;top:30px;font-weight:700;font-size:22px;letter-spacing:6px;color:rgba(255,212,0,.8)}
.vcard .ix b{color:#cfcfcf;margin-left:12px}
.vcard .nm{position:absolute;left:34px;top:70px;font-family:Anton;font-size:84px;line-height:1.05;white-space:nowrap}
.vcard .ef{position:absolute;left:38px;top:186px;width:620px;font-weight:600;font-size:34px;line-height:1.2;color:#e6e6e6}
.vcard .lv{position:absolute;right:36px;top:28px;text-align:right;font-weight:700;font-size:20px;letter-spacing:4px;color:#9a9a9a}
.vcard .lv b{display:block;font-family:Anton;font-weight:400;font-size:64px;letter-spacing:1px;color:var(--y);line-height:1}
.wipe{position:absolute;top:0;bottom:0;width:260px;background:linear-gradient(90deg,transparent,rgba(255,226,120,.95) 45%,#fff 50%,rgba(255,226,120,.95) 55%,transparent);
  filter:blur(6px);transform:skewX(-14deg);opacity:0}
.flash{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(255,220,120,.35),transparent 60%);opacity:0}
.prog{position:absolute;left:60px;top:470px;display:flex;gap:10px}
.prog i{display:block;width:70px;height:6px;background:rgba(255,255,255,.18)}
.prog i b{display:block;height:100%;background:var(--y);width:0}
"""


def page(items, d):
    segs = ''.join(
        f'<div class="seg" id="s{k}" style="position:absolute;inset:0;opacity:0">'
        f'<div class="stage"><div class="wrap" id="w{k}"><img class="g" src="/weapons/{it["image"]}">'
        f'<div class="shine" id="sh{k}" style="-webkit-mask-image:url(/weapons/{it["image"]})"></div></div></div>'
        f'<div class="vcard hud" id="c{k}"><div class="ix">{it["n"]:02d}/28<b>{E(it["weapon"].upper())}</b></div>'
        f'<div class="nm fit" style="left:34px" data-size="84" data-max="620"><span class="gold">{E(it["apex"].upper())}</span></div>'
        f'<div class="lv">MAX LVL<b>{it["level"]}</b></div><div class="ef">{E(it["effect"])}</div></div></div>'
        for k, it in enumerate(items))
    prog = ''.join(f'<i><b id="p{k}"></b></i>' for k in range(len(items)))
    body = (R.FRAME.format(game=E(d['game']), badge=E(d['badge'])).replace('top:134px', 'top:214px').replace('top:118px', 'top:196px')
            + '<div class="kicker" style="top:300px;left:60px;font-size:28px;letter-spacing:12px">EVERY APEX IN MW4</div>'
            + '<div class="fit" style="top:345px" data-size="104" data-max="860"><span class="gr w">APEX</span><span class="gr gold" style="margin-left:24px">SHOWCASE</span></div>'
            + f'<div class="prog">{prog}</div>'
            + '<div class="shadow" id="shd"></div><div class="ring"></div>' + segs
            + '<div class="flash" id="fl"></div><div class="wipe" id="wp"></div>')
    js = f"""<script>
const N={len(items)},SEG={SEG},TR={TR};
const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2, cl=x=>Math.max(0,Math.min(1,x));
function draw(t){{
 const k=Math.min(N-1,Math.floor(t/SEG)), lt=t-k*SEG;
 for(let i=0;i<N;i++){{
  const s=document.getElementById('s'+i), w=document.getElementById('w'+i), c=document.getElementById('c'+i), sh=document.getElementById('sh'+i);
  const u=t-i*SEG; let op=0, x=0, blur=0;
  if(u>=-TR/2 && u<SEG+TR/2){{
    const inn=cl((u+TR/2)/TR), out=cl((u-(SEG-TR/2))/TR);
    op = (i==0?1:ease(inn)) * (i==N-1?1:1-ease(out));
    x = (i==0?0:(1-ease(inn))*700) - (i==N-1?0:ease(out)*700);
    blur = (i==0?0:(1-inn)*14) + (i==N-1?0:out*14);
  }}
  s.style.opacity=op;
  const lu=Math.max(0,Math.min(SEG,u));
  const ang=26*Math.sin(2*Math.PI*lu/SEG*1.0 - Math.PI/2);  // -26 -> +26 -> -26 deg turn
  const sc=0.94+0.08*ease(lu/SEG), fy=10*Math.sin(2*Math.PI*lu/2.5);
  w.style.transform=`translate(${{x}}px,${{fy}}px) rotateY(${{ang}}deg) rotateZ(-3deg) scale(${{sc}})`;
  w.style.filter=`blur(${{blur}}px)`;
  const sp=(lu%2.5)/2.5;  // light sweep every 2.5 s
  sh.style.background=`linear-gradient(105deg,transparent ${{sp*160-40}}%,rgba(255,236,170,.55) ${{sp*160-25}}%,transparent ${{sp*160-10}}%)`;
  const ci=cl((u-0.25)/0.45), co=(i==N-1?0:cl((u-(SEG-TR/2))/TR));
  c.style.opacity=ease(ci)*(1-co); c.style.transform=`translateY(${{(1-ease(ci))*80}}px)`;
  document.getElementById('p'+i).style.width=(cl(u/SEG)*100)+'%';
 }}
 const b=t-(k+1)*SEG, tb=(k+1<N&&Math.abs(b)<TR/2)?b: (Math.abs(t-k*SEG)<TR/2&&k>0? t-k*SEG : 9);
 const wp=document.getElementById('wp'), fl=document.getElementById('fl');
 if(Math.abs(tb)<TR/2){{const p=(tb+TR/2)/TR; wp.style.opacity=1; wp.style.left=(-300+p*1700)+'px'; fl.style.opacity=Math.sin(p*Math.PI)*.9;}}
 else {{wp.style.opacity=0; fl.style.opacity=0;}}
 const lu=t-k*SEG; document.getElementById('shd').style.transform=`scaleX(${{0.8+0.2*Math.cos(26*Math.sin(2*Math.PI*lu/SEG-Math.PI/2)*Math.PI/180)}})`;
}}
</script>"""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}'
            + R.FITJS.replace('document.body.dataset.ready=1', 'draw(0);document.body.dataset.ready=1') + js + '</body></html>')


def main(data_path, names, out):
    d = json.load(open(data_path))
    by = {it['apex']: it for it in d['items']}
    items = [by[n.strip()] for n in names.split(',')]
    tmp = os.path.join(R.HERE, '_build', 'video'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    open(os.path.join(R.HERE, '_build', 'apex_video.html'), 'w').write(page(items, d))
    total = SEG * len(items); n = int(total * FPS)
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/apex_video.html')
        pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(400)
        for f in range(n):
            pg.evaluate(f'draw({f / FPS})')
            pg.screenshot(path=os.path.join(tmp, f'{f:05d}.png'), type='png')
        b.close()
    srv.shutdown()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'),
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    print(out, n, 'frames')


if __name__ == '__main__':
    main(*sys.argv[1:])
