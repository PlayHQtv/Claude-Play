"""PlayHQ carousel -> motion video: "EVERY MW4 KILLSTREAK" (9:16, 1080x1920, 60 fps).

Modern motion design built from the verified carousel data:
  - beat grid 120 BPM: every cut, card and counter step lands on a beat or 8th note
  - expo / back easing, masked line reveals, staggered card fly-ins with an image wipe + Ken Burns
  - odometer kill counter + segmented kill meter that fills tier by tier
  - nuke finale: riser, screen shake, chromatic aberration, shockwave, flash, red grade
  - real motion blur: SUB sub-frames per output frame, averaged with ffmpeg tmix
  - synthesized sound track (kick, hats, sidechained bass, whooshes, ticks, riser, boom), film grain, animated logo
Usage: python3 streak_video.py data/2026-11-05-mw4-killstreaks.json out.mp4 [--fast]
"""
import json, os, sys, subprocess, shutil, wave
import numpy as np
import render as R

HERE = R.HERE
VF = os.path.join(HERE, '..', 'video-frame')
sys.path.insert(0, VF)
import sfx, logo_anim  # noqa: E402

E = R.E
FPS = 60
BEAT = 0.5
T_HOOK, TIER = 2.5, 3.0
NS = T_HOOK + 5 * TIER          # nuke start 17.5
BOOM = NS + 1.5                 # 19.0
NE = BOOM + 3.0                 # 22.0
END = NE + 3.5                  # 25.5
KILLS = [4, 6, 8, 10, 12]

CSS = R.CSS.replace('height:1440px', 'height:1920px').replace('top:134px', 'top:205px') + """
#cam{position:absolute;inset:0;transform-origin:540px 900px}
.logo{display:none}
.hk{position:absolute;left:62px;font-weight:700;font-size:28px;letter-spacing:10px;color:var(--y)}
.ln{position:absolute;left:52px;overflow:hidden;padding:4px 14px 8px 10px;font-family:Anton;line-height:1;letter-spacing:3px;white-space:nowrap}
.ln>span{display:inline-block}
.mq{position:absolute;left:-260px;width:1600px;top:900px;height:470px;transform:rotate(-8deg);
  -webkit-mask-image:linear-gradient(90deg,transparent 8%,#000 26%,#000 74%,transparent 92%)}
.row{position:absolute;left:0;display:flex;gap:18px;white-space:nowrap}
.row i{flex:none;display:block;width:300px;height:169px;background-size:cover;background-position:center;border:2px solid rgba(255,212,0,.45);
  clip-path:polygon(0 0,100% 0,100% 82%,88% 100%,0 100%);filter:saturate(.85) brightness(.85)}
#meter{position:absolute;left:0;right:0;top:490px;height:170px}
.odo{position:absolute;left:58px;top:0;display:flex;height:150px;overflow:hidden}
.dg{width:86px;height:150px;overflow:hidden}
.dg .st{display:flex;flex-direction:column}
.dg .st b{display:block;height:150px;font-family:Anton;font-weight:400;font-size:150px;line-height:150px;text-align:center;
  color:var(--dc,#ffd400);text-shadow:0 0 28px var(--dg,rgba(255,212,0,.45))}
.kl{position:absolute;left:240px;top:22px;font-family:Anton;font-size:42px;letter-spacing:4px;color:#e9e9e9}
.kl small{display:block;font-family:Raj;font-weight:700;font-size:20px;letter-spacing:5px;color:#9a9a9a}
.bar{position:absolute;left:250px;width:690px;top:112px;height:14px;background:rgba(255,255,255,.1);clip-path:polygon(0 0,100% 0,calc(100% - 10px) 100%,0 100%)}
.bar .f{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,#b8862a,#ffd400 70%,#fff3c4);box-shadow:0 0 20px rgba(255,212,0,.8)}
.mk{position:absolute;top:136px;font-weight:700;font-size:21px;letter-spacing:2px;color:#6d6d6d;transform:translateX(-50%)}
.mk::before{content:"";position:absolute;left:50%;top:-30px;width:3px;height:22px;margin-left:-1px;background:currentColor}
.kc{position:absolute;left:50px;width:880px;height:188px;opacity:0}
.kc .im{position:absolute;left:10px;top:9px;width:300px;height:170px;overflow:hidden;
  clip-path:polygon(0 0,100% 0,100% 82%,88% 100%,0 100%)}
.kc .im i{position:absolute;inset:0;background-size:cover;background-position:center}
.kc .im::after{content:"";position:absolute;inset:0;border:2px solid rgba(255,212,0,.6)}
.kc .kb{position:absolute;left:10px;top:9px;width:84px;height:84px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);color:#140f00;clip-path:polygon(0 0,100% 0,100% 74%,74% 100%,0 100%);transform-origin:20px 20px}
.kc .kb b{font-family:Anton;font-weight:400;font-size:50px;line-height:1}
.kc .kb small{font-weight:700;font-size:13px;letter-spacing:3px}
.kc .tx{position:absolute;left:334px;right:22px;top:16px}
.kc .nm{font-family:Anton;font-size:48px;line-height:1.05;letter-spacing:1px;color:#f3f3f3;white-space:nowrap}
.kc .cp{display:flex;gap:10px;margin-top:6px}
.kc .cp span{font-weight:700;font-size:19px;letter-spacing:3px;padding:3px 10px}
.kc .lv{color:#111;background:#3ddc84}.kc .nt{color:var(--y);border:1px solid rgba(255,212,0,.5)}
.kc .ds{font-weight:600;font-size:27px;line-height:1.2;color:#d2d2d2;margin-top:7px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.kc .sw{position:absolute;top:0;bottom:0;width:38%;left:0;background:linear-gradient(100deg,transparent,rgba(255,236,170,.22) 50%,transparent);mix-blend-mode:screen}
.big30{position:absolute;left:0;right:0;top:560px;text-align:center;font-family:Anton;font-size:900px;line-height:1;color:transparent;
  -webkit-text-stroke:3px rgba(255,90,60,.5);opacity:0}
.shock{position:absolute;left:540px;top:820px;width:400px;height:400px;margin:-200px 0 0 -200px;border-radius:50%;
  border:10px solid rgba(255,140,90,.9);box-shadow:0 0 60px rgba(255,80,40,.8),inset 0 0 60px rgba(255,80,40,.6);opacity:0}
.nt{position:absolute;left:0;right:0;top:720px;text-align:center;font-family:Anton;font-size:146px;line-height:1;letter-spacing:3px;color:#fff;opacity:0}
.nr{position:absolute;left:70px;width:840px;height:96px;display:flex;align-items:center;gap:22px;padding:0 28px;opacity:0}
.nr b{flex:none;font-family:Anton;font-weight:400;font-size:38px;color:#ff5a46;width:56px;text-align:center}
.nr p{font-weight:700;font-size:33px;line-height:1.15;color:#eee}
.tp{position:absolute;left:50px;width:880px;height:158px;padding:24px 30px;opacity:0}
.tp b{display:block;font-family:Anton;font-weight:400;font-size:46px;letter-spacing:2px;color:var(--y)}
.tp p{font-weight:700;font-size:31px;line-height:1.2;color:#e6e6e6;margin-top:4px}
.save{position:absolute;left:62px;top:1290px;display:flex;gap:16px;opacity:0}
.save span{font-family:Anton;font-size:40px;letter-spacing:3px;padding:12px 26px;color:#140f00;background:linear-gradient(135deg,#ffe88f,#e9c062 50%,#b8862a);
  clip-path:polygon(0 0,100% 0,calc(100% - 16px) 100%,0 100%)}
.save span.o{background:none;color:#fff;border:2px solid rgba(255,255,255,.5);clip-path:none}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
#red{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(255,40,20,.18),rgba(120,0,0,.55) 75%);opacity:0;mix-blend-mode:screen}
#tint{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 45%,rgba(90,0,0,.7));opacity:0}
"""


def tiers(d):
    out = []
    for t in d['tiers']:
        st = [s for s in t['streaks'] if not s.get('nuke')]
        out.append({'title': t['title'].replace(' + THE NUKE', ' STREAKS').replace('KILLS STREAKS', 'KILL STREAKS'), 'sub': t['sub'], 'streaks': st})
    return out


def kc(s, i, j):
    lv = f'<span class="lv">UNLOCK LV {s["lv"]}</span>' if s.get('lv') else ''
    nt = f'<span class="nt">{E(s["note"])}</span>' if s.get('note') else ''
    return (f'<div class="kc hud" id="c{i}_{j}" style="top:{700 + j * 206}px">'
            f'<div class="im"><i id="ci{i}_{j}" style="background-image:url(/_build/ks/{s["img"]}.jpg)"></i></div>'
            f'<div class="kb" id="cb{i}_{j}"><b>{E(s["kills"])}</b><small>KILLS</small></div>'
            f'<div class="tx" id="ct{i}_{j}"><div class="nm">{E(s["name"].upper())}</div><div class="cp">{lv}{nt}</div>'
            f'<div class="ds">{E(s["desc"])}</div></div><div class="sw" id="cs{i}_{j}"></div></div>')


def header(key, kick, title, cls='w', size=104, top=318):
    return (f'<div class="hk" id="hk{key}" style="top:{top - 44}px;opacity:0">{E(kick)}</div>'
            f'<div class="ln fit" id="hl{key}" style="top:{top}px" data-size="{size}" data-max="900"><span class="gr {cls}">{E(title)}</span></div>')


def page(d):
    T = tiers(d)
    imgs = [s['img'] for t in d['tiers'] for s in t['streaks'] if s.get('img')]
    r1 = ''.join(f'<i style="background-image:url(/_build/ks/{n}.jpg)"></i>' for n in (imgs[:9] * 3))
    r2 = ''.join(f'<i style="background-image:url(/_build/ks/{n}.jpg)"></i>' for n in (imgs[8:] * 3))
    frame = R.FRAME.format(game=E(d['game']), badge=E(d['badge']))
    hook = ('<div id="hook">'
            '<div class="hk" id="hkk" style="top:300px">MW4 MULTIPLAYER · ALL 17 + THE NUKE</div>'
            '<div class="ln fit" id="h1" style="top:340px" data-size="250" data-max="900"><span class="gr gold">EVERY</span></div>'
            '<div class="ln fit" id="h2" style="top:600px" data-size="168" data-max="900"><span class="gr w">KILLSTREAK</span></div>'
            '<div class="hk" id="h3" style="top:800px;font-size:30px;letter-spacing:8px;color:#e6e6e6">FROM 4 KILLS TO THE NUKE</div>'
            f'<div class="mq" id="mq"><div class="row" id="r1" style="top:40px">{r1}</div><div class="row" id="r2" style="top:230px">{r2}</div></div></div>')
    marks = ''.join(f'<div class="mk" id="mk{k}" style="left:{250 + 690 * f}px">{lab}</div>'
                    for k, (f, lab) in enumerate([(.1, '4'), (.26, '6'), (.42, '8'), (.58, '10'), (.74, '12'), (.985, 'NUKE')]))
    digits = ''.join(f'<b>{n % 10}</b>' for n in range(11))
    meter = (f'<div id="meter" style="opacity:0"><div class="odo"><div class="dg"><div class="st" id="d1">{digits}</div></div>'
             f'<div class="dg"><div class="st" id="d0">{digits}</div></div></div>'
             f'<div class="kl">KILLS<small>IN ONE LIFE</small></div><div class="bar"><div class="f" id="bf"></div></div>{marks}</div>')
    heads = ''.join(header(i, t['sub'], t['title']) for i, t in enumerate(T))
    heads += header('n', 'TOP OF THE CHAIN', '30 KILLS. ONE LIFE.', 'w', 104)
    heads += header('o', 'BEFORE YOU PICK', '2 RULES MOST MISS', 'gold', 104)
    cards = ''.join(kc(s, i, j) for i, t in enumerate(T) for j, s in enumerate(t['streaks']))
    nk = next(s for t in d['tiers'] for s in t['streaks'] if s.get('nuke'))
    rows = ['Only gun, equipment + field upgrade kills count', 'No streak slot needed: always active', 'Ends the match: your team wins']
    nuke = ('<div class="big30" id="b30">30</div><div class="shock" id="sw"></div><div class="nt" id="nt">TACTICAL NUKE</div>'
            + ''.join(f'<div class="nr hud" id="nr{k}" style="top:{960 + k * 116}px"><b>{k + 1}</b><p>{E(r)}</p></div>' for k, r in enumerate(rows)))
    ru = dict(d['rules']['items'])
    tips = [('HARDLINE = −1 KILL', 'Perk 2 (Lv 4): every streak costs one kill less.'),
            ('SMART STREAKS', 'Flags, Hardpoint time + Data Spike plants fill your meter too.')]
    assert 'HARDLINE' in ru and 'SMART STREAKS' in ru
    out = (''.join(f'<div class="tp hud" id="tp{k}" style="top:{520 + k * 180}px"><b>{E(a)}</b><p>{E(b)}</p></div>' for k, (a, b) in enumerate(tips))
           + '<div class="ln fit" id="q1" style="top:900px" data-size="140" data-max="900"><span class="gr w">YOUR 3</span></div>'
           + '<div class="ln fit" id="q2" style="top:1050px" data-size="140" data-max="900"><span class="gr gold">STREAKS?</span></div>'
           + '<div class="save" id="sv"><span>COMMENT ↓</span><span class="o">SAVE + FOLLOW</span></div>')
    cfg = {'T_HOOK': T_HOOK, 'TIER': TIER, 'NS': NS, 'BOOM': BOOM, 'NE': NE, 'END': END, 'K': KILLS, 'NC': [len(t['streaks']) for t in T]}
    body = (f'<div id="cam">{frame}{hook}{meter}{heads}{cards}{nuke}{out}</div><div id="tint"></div><div id="red"></div><div id="flash"></div>')
    assert nk['kills'] == '30'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}'
            f'<script>const C={json.dumps(cfg)};</script><script>{JS}</script>'
            + R.FITJS.replace('document.body.dataset.ready=1', 'draw(0);document.body.dataset.ready=1') + '</body></html>')


JS = r"""
const $=id=>document.getElementById(id), cl=x=>Math.max(0,Math.min(1,x)), seg=(t,a,d)=>cl((t-a)/d), lerp=(a,b,x)=>a+(b-a)*x;
const eo=x=>x>=1?1:1-Math.pow(2,-10*x), ei=x=>x<=0?0:Math.pow(2,10*x-10), io=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
const bo=x=>{const c1=2.2,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const S=i=>C.T_HOOK+i*C.TIER;
function V(t){ let v=0;
  for(let i=0;i<5;i++) if(t>=S(i)) v=lerp(i?C.K[i-1]:0,C.K[i],seg(t,S(i)+0.05,0.4));
  if(t>=C.NS+0.1) v=lerp(12,30,Math.pow(seg(t,C.NS+0.1,C.BOOM-C.NS-0.1),2.3));
  return v; }
function odo(v){ const k=Math.floor(v+1e-6), f=v-k, d=k+io(f);
  $('d0').style.transform=`translateY(${-(d%10)*150}px)`;
  const tp=Math.floor(d/10)+Math.max(0,(d%10)-9); $('d1').style.transform=`translateY(${-tp*150}px)`;
  $('d1').parentNode.style.opacity=tp<0.5?0.18:1; }
const FM=[[0,0],[4,.1],[6,.26],[8,.42],[10,.58],[12,.74],[30,1]];
function frac(v){ for(let i=1;i<FM.length;i++) if(v<=FM[i][0]) return lerp(FM[i-1][1],FM[i][1],(v-FM[i-1][0])/(FM[i][0]-FM[i-1][0])); return 1; }
function line(id,tin,tout,dur=0.5){ const e=$(id).firstElementChild, a=eo(seg(tin<0?0:tin,0,1)), p=eo(seg(window._t,tin,dur)), q=ei(seg(window._t,tout,0.3));
  e.style.transform=`translateY(${(1-p)*115-q*115}%) skewY(${(1-p)*6}deg)`; $(id).style.opacity=(window._t>=tin-0.02&&window._t<tout+0.32)?1:0; }
function kick(id,tin,tout){ const p=eo(seg(window._t,tin,0.45)), q=ei(seg(window._t,tout,0.3)), e=$(id);
  e.style.opacity=Math.min(p,1-q); e.style.transform=`translateX(${(1-p)*-40+q*40}px)`; e.style.letterSpacing=(10+(1-p)*14)+'px'; }
function head(key,tin,tout){ kick('hk'+key,tin,tout); line('hl'+key,tin+0.06,tout); }
function draw(t){ window._t=t;
  // camera: slow push + punch on every tier / boom + shake
  let punch=0; for(let i=0;i<5;i++){const u=t-S(i); if(u>=0) punch+=0.022*Math.exp(-u*7);}
  if(t>=C.BOOM) punch+=0.08*Math.exp(-(t-C.BOOM)*4);
  let amp=0; if(t>=C.NS&&t<C.BOOM) amp=7*Math.pow(seg(t,C.NS,C.BOOM-C.NS),2); if(t>=C.BOOM) amp=30*Math.exp(-(t-C.BOOM)*4.5);
  const sx=amp*(Math.sin(t*97)+Math.sin(t*61.3))/2, sy=amp*(Math.sin(t*83.1)+Math.cos(t*47.7))/2, rz=amp*0.03*Math.sin(t*71);
  $('cam').style.transform=`translate(${sx}px,${sy}px) rotate(${rz}deg) scale(${1+0.018*t/C.END+punch})`;
  document.querySelector('.topo').style.backgroundPosition=`${-t*14}px ${t*9}px`;
  // HOOK
  const ho=eo(seg(t,C.T_HOOK-0.32,0.34)), hk=$('hook');
  hk.style.opacity=t<C.T_HOOK+0.05?1-ho:0; hk.style.transform=`translateY(${-ho*90}px) scale(${1+ho*0.08})`; hk.style.filter=`blur(${ho*12}px)`;
  kick('hkk',0,99); line('h1',0.0,99,0.45); line('h2',0.25,99,0.45);
  const h3=eo(seg(t,0.55,0.4)); $('h3').style.opacity=h3; $('h3').style.transform=`translateY(${(1-h3)*24}px)`;
  const mi=eo(seg(t,0,0.6)); $('mq').style.opacity=mi;
  $('r1').style.transform=`translateX(${-150-t*170}px)`; $('r2').style.transform=`translateX(${-900+t*170}px)`;
  // METER
  const mIn=eo(seg(t,C.T_HOOK-0.15,0.45)), mOut=ei(seg(t,C.NE-0.1,0.3)), m=$('meter');
  m.style.opacity=Math.min(mIn,1-mOut); m.style.transform=`translateY(${(1-mIn)*40-mOut*40}px)`;
  const v=V(t); odo(v); $('bf').style.width=(frac(v)*100)+'%';
  const nuk=seg(t,C.NS,0.6);
  m.style.setProperty('--dc',`rgb(255,${Math.round(lerp(212,75,nuk))},${Math.round(lerp(0,62,nuk))})`);
  m.style.setProperty('--dg',`rgba(255,${Math.round(lerp(212,60,nuk))},${Math.round(lerp(0,40,nuk))},.6)`);
  $('bf').style.filter=`hue-rotate(${-nuk*45}deg) saturate(${1+nuk})`;
  [4,6,8,10,12,30].forEach((k,i)=>{const on=v>=k-0.01; const e=$('mk'+i); e.style.color=on?(k==30?'#ff5a46':'#ffd400'):'#6d6d6d'; e.style.textShadow=on?'0 0 14px currentColor':'none';});
  // TIERS
  for(let i=0;i<5;i++){ const s=S(i), e=s+C.TIER-0.36; head(i,s,e);
    for(let j=0;j<C.NC[i];j++){ const tin=s+0.22+j*0.25, c=$(`c${i}_${j}`);
      const p=eo(seg(t,tin,0.6)), q=ei(seg(t,e+j*0.04,0.32));
      c.style.opacity=(t>=tin&&t<e+0.5)?1:0;
      c.style.transform=`translateX(${(1-p)*1150-q*1150}px) skewX(${(1-p)*-12+q*12}deg)`;
      const w=eo(seg(t,tin+0.1,0.5)); $(`ci${i}_${j}`).parentNode.style.clipPath=`inset(0 ${(1-w)*100}% 0 0)`;
      $(`ci${i}_${j}`).style.transform=`scale(${1.2-0.16*seg(t,tin,2.6)})`;
      const b=bo(seg(t,tin+0.28,0.4)); $(`cb${i}_${j}`).style.transform=`scale(${b}) rotate(${(1-b)*-25}deg)`;
      const x=eo(seg(t,tin+0.12,0.55)); const tx=$(`ct${i}_${j}`); tx.style.opacity=x; tx.style.transform=`translateX(${(1-x)*70}px)`;
      $(`cs${i}_${j}`).style.transform=`translateX(${lerp(-120,300,seg(t,tin+0.5,0.7))}%) skewX(-18deg)`; } }
  // NUKE
  head('n',C.NS,C.NE-0.36);
  const b=seg(t,C.BOOM,9), nt=$('nt');
  const ns=eo(seg(t,C.BOOM,0.35)), nq=ei(seg(t,C.NE-0.36,0.3));
  nt.style.opacity=t>=C.BOOM?1-nq:0; nt.style.transform=`scale(${lerp(2.4,1,ns)*(1+0.012*Math.sin(t*9))}) translateY(${-nq*60}px)`;
  const ca=t>=C.BOOM?(4+22*Math.exp(-(t-C.BOOM)*5)):0;
  nt.style.textShadow=`${ca}px 0 rgba(255,40,40,.9),${-ca}px 0 rgba(0,220,255,.75),0 0 60px rgba(255,70,40,.75)`;
  const sw=seg(t,C.BOOM,0.9); $('sw').style.opacity=t>=C.BOOM?(1-sw)*0.95:0; $('sw').style.transform=`scale(${0.2+eo(sw)*4.2})`;
  const b3=$('b30'); b3.style.opacity=t>=C.BOOM?0.55*eo(seg(t,C.BOOM,0.5))*(1-nq):0; b3.style.transform=`scale(${1.25-0.18*eo(seg(t,C.BOOM,3))})`;
  for(let k=0;k<3;k++){ const tin=C.BOOM+0.45+k*0.25, p=eo(seg(t,tin,0.5)), q=ei(seg(t,C.NE-0.36+k*0.04,0.3)), r=$('nr'+k);
    r.style.opacity=Math.min(p,1-q); r.style.transform=`translateX(${(1-p)*-900+q*900}px) skewX(${(1-p)*12}deg)`; }
  $('flash').style.opacity=t>=C.BOOM?Math.exp(-(t-C.BOOM)*9):0;
  let tint=0; for(let i=0;i<5;i++){const u=t-S(i); if(u>=0) tint=Math.max(tint,0.12*Math.exp(-u*8));}
  $('red').style.opacity=t>=C.NS?Math.min(seg(t,C.NS,1.5)*0.55,1-seg(t,C.NE-0.2,0.5))+(t>=C.BOOM?0.35*Math.exp(-(t-C.BOOM)*3):0):0;
  $('tint').style.opacity=t>=C.NS?(1-seg(t,C.NE-0.2,0.5))*0.8:0;
  // OUTRO
  head('o',C.NE,99);
  for(let k=0;k<2;k++){ const tin=C.NE+0.3+k*0.25, p=eo(seg(t,tin,0.55)), r=$('tp'+k);
    r.style.opacity=p; r.style.transform=`translateX(${(1-p)*1100}px) skewX(${(1-p)*-12}deg)`; }
  line('q1',C.NE+1.0,99,0.45); line('q2',C.NE+1.25,99,0.45);
  const sv=bo(seg(t,C.NE+1.6,0.45)); $('sv').style.opacity=cl(sv); $('sv').style.transform=`scale(${0.6+0.4*sv})`; $('sv').style.transformOrigin='0 50%';
}
"""


# ---------------------------------------------------------------- audio
def soundtrack(path, d):
    SR = sfx.SR; n = int(END * SR); s = np.zeros(n); t = np.arange(n) / SR
    rng = np.random.default_rng(7)

    def put(x, at, g):
        i = int(at * SR); j = min(n, i + len(x))
        if i < n: s[i:j] += x[:j - i] * g

    hat = np.diff(rng.standard_normal(int(0.05 * SR) + 1)) * sfx._env(int(0.05 * SR), 0.001, 0.012)
    kick = sfx._tone(0.4, 150, 42, 0.11)
    beats = [b for b in np.arange(0, END - 0.4, BEAT) if not (NS - 0.01 <= b < BOOM)]
    duck = np.ones(n)
    for b in beats:
        put(kick, b, 0.95)
        put(hat, b + BEAT / 2, 0.16)
        i = int(b * SR); k = np.arange(min(n - i, int(0.35 * SR))); duck[i:i + len(k)] = np.minimum(duck[i:i + len(k)], 1 - 0.75 * np.exp(-k / (0.09 * SR)))
    # bass line (A1 A1 F1 G1 per 2 s), sidechained to the kick
    notes = [55.0, 55.0, 43.65, 49.0]
    f = np.array([notes[int(x // 2) % 4] for x in t])
    bass = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.35 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    gate = np.ones(n); gate[(t >= NS) & (t < BOOM)] = 0.25
    s += bass * duck * gate * 0.22 * np.clip(np.minimum(t / 0.3, (END - t) / 0.6), 0, 1)
    # hook
    put(sfx._tone(0.6, 90, 35, 0.2), 0, 1.0); put(sfx._noise_sweep(0.3, 6000, 400), 0, 0.4)
    put(sfx._noise_sweep(0.35, 400, 6000), T_HOOK - 0.35, 0.45)
    # tiers
    for i in range(5):
        st = T_HOOK + i * TIER
        put(sfx._tone(0.5, 85, 38, 0.16), st, 0.8); put(sfx._noise_sweep(0.25, 5000, 800), st, 0.3)
        prev = KILLS[i - 1] if i else 0
        for k in range(KILLS[i] - prev):
            put(sfx._tone(0.025, 3200, 3200, 0.005), st + 0.05 + (k + 0.5) / (KILLS[i] - prev) * 0.4, 0.28)
        nc = len(d['tiers'][i]['streaks']) - (1 if i == 4 else 0)
        for j in range(nc):
            tin = st + 0.22 + j * 0.25
            put(sfx._noise_sweep(0.22, 1200, 5200), tin - 0.05, 0.22)
            put(sfx._tone(0.09, 1500, 900, 0.03), tin + 0.3, 0.38)
        if i < 4:
            put(sfx._noise_sweep(0.3, 5000, 700), st + TIER - 0.36, 0.25)
    # nuke: riser with accelerating ticks, then boom
    rl = BOOM - NS
    r = sfx._noise_sweep(rl, 250, 7000) * np.linspace(0.2, 1, int(rl * SR)) ** 2
    put(r, NS, 0.75)
    tr = np.arange(int(rl * SR)) / SR
    put(np.sin(2 * np.pi * np.cumsum(100 + 300 * (tr / rl) ** 2) / SR) * (tr / rl) ** 2, NS, 0.25)
    for k in range(18):
        x = ((k + 1) / 18) ** (1 / 2.3)
        put(sfx._tone(0.025, 3400, 3400, 0.005), NS + 0.1 + x * (rl - 0.1), 0.3)
    bl = int(1.8 * SR); bn = rng.standard_normal(bl)
    bn = np.convolve(bn, np.ones(40) / 40, 'same') * np.exp(-np.arange(bl) / (0.35 * SR))
    put(sfx._tone(1.8, 70, 26, 0.7), BOOM, 1.5); put(bn / (np.abs(bn).max() + 1e-9), BOOM, 0.9)
    put(sfx._noise_sweep(0.3, 6000, 500), NE - 0.36, 0.3)
    # outro
    for k in range(2):
        put(sfx._noise_sweep(0.22, 1200, 5200), NE + 0.3 + k * 0.25 - 0.05, 0.22)
    hit = NE + 1.6
    put(sfx._tone(0.7, 880, 880, 0.18) + 0.7 * sfx._tone(0.7, 1320, 1320, 0.15), hit, 0.35)
    s = np.tanh(s / (np.abs(s).max() + 1e-9) * 1.6) * 0.89
    st2 = (np.stack([s, s], 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st2.tobytes())


def logo_mov(path):
    if os.path.exists(path):
        return path
    L = logo_anim.layers(); tmp = path + '_f'; os.makedirs(tmp, exist_ok=True)
    for i in range(logo_anim.FPS * logo_anim.SECS):
        logo_anim.frame(i, L, rgba=True).save(f'{tmp}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(logo_anim.FPS), '-i', f'{tmp}/%04d.png', '-c:v', 'png', path], check=True)
    shutil.rmtree(tmp)
    return path


def main(data_path, out, *flags):
    fast = '--fast' in flags
    sub = 1 if fast else 2
    d = json.load(open(data_path))
    b = os.path.join(HERE, '_build'); tmp = os.path.join(b, 'svid'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    open(os.path.join(b, 'streak_video.html'), 'w').write(page(d))
    rate = FPS * sub; n = int(END * rate)
    srv = R.serve(HERE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/streak_video.html')
        pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(500)
        for f in range(0, n, 6 if fast else 1):
            pg.evaluate(f'draw({f / rate})')
            pg.screenshot(path=os.path.join(tmp, f'{f // (6 if fast else 1):05d}.jpg'), type='jpeg', quality=96)
        br.close()
    srv.shutdown()
    wav = os.path.join(b, 'streak_video.wav'); soundtrack(wav, d)
    lg = logo_mov(os.path.join(b, 'logo_rgba.mov'))
    if fast:
        vf_in = f'-framerate {rate / 6}'
        chain = f'[0:v]fps={FPS}[v0]'
    else:
        vf_in = f'-framerate {rate}'
        chain = f'[0:v]tmix=frames={sub},framestep={sub},setpts=N/{FPS}/TB[v0]'
    fc = (chain + f';[v0]noise=c0s=5:allf=t[v1];[2:v]fps={FPS}[lg];[v1][lg]overlay=880:140:shortest=0:eof_action=pass,format=yuv420p[v]')
    cmd = (['ffmpeg', '-y', '-loglevel', 'error'] + vf_in.split() + ['-i', os.path.join(tmp, '%05d.jpg'), '-i', wav,
           '-stream_loop', '-1', '-i', lg, '-filter_complex', fc, '-map', '[v]', '-map', '1:a', '-t', str(END),
           '-r', str(FPS), '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out])
    subprocess.run(cmd, check=True)
    print(out, n, 'renders')


if __name__ == '__main__':
    main(*sys.argv[1:])
