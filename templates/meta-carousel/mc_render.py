"""PlayHQ MINECRAFT carousel template (user 18.11.2026: "Vorlage nach den Regeln aber in dem Stil von Minecraft").
Blocky pixel look: pixel display font with hard block shadow, bevelled GUI panels and item slots, yellow splash text,
blocky backgrounds. Rules (Minecraft Usage Guidelines): NO Minecraft logo, NO official marketing/package artwork,
NO Mojang characters drawn by us – backgrounds are own gameplay screenshots or own pixel art (mc_art.py);
the word MINECRAFT only as plain text; every post carries the disclaimer
"NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT."
Usage: python3 mc_render.py data/<file>.json <out_dir>. Images: _build/mc/ (private) or assets/."""
import json, os, sys
import render as R

E = R.E
DISC = 'NOT AN OFFICIAL MINECRAFT PRODUCT.<br>NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.'
CSS = """
@font-face{font-family:PX;src:url(/assets/fonts/PixelifySans-700.woff2);font-weight:700}
@font-face{font-family:PX;src:url(/assets/fonts/PixelifySans-500.woff2);font-weight:500}
@font-face{font-family:P2;src:url(/assets/fonts/PressStart2P.woff2)}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-600.woff2);font-weight:600}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-700.woff2);font-weight:700}
@font-face{font-family:IT;src:url(/assets/fonts/InterTight-800.woff2);font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
:root{--g:#62b23f;--gd:#3c7d24;--y:#ffe14d;--sl:#c6c6c6;--ink:#141418}
html,body{width:1080px;height:1440px;overflow:hidden}
body{position:relative;background:var(--ink);color:#fff;font-family:IT;-webkit-font-smoothing:antialiased;image-rendering:pixelated}
.bg{position:absolute;inset:0;background-size:cover;background-position:center top;image-rendering:pixelated}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,14,.55) 0%,rgba(10,10,14,.05) 26%,rgba(10,10,14,.15) 44%,rgba(10,10,14,.86) 66%,rgba(10,10,14,.96) 100%)}
.px{font-family:PX;font-weight:700;line-height:.92;text-shadow:7px 7px 0 #2a2a2a;letter-spacing:1px}
.px em{font-style:normal;color:var(--y)}
.brand{position:absolute;left:56px;top:128px;display:flex;align-items:center;gap:16px}
.brand b{font-family:PX;font-weight:700;font-size:58px;color:#fff;text-shadow:5px 5px 0 #2a2a2a;letter-spacing:2px}
.tile{font-family:P2;font-size:13px;line-height:1.7;letter-spacing:1px;color:#fff;padding:10px 14px;background:#6b6b6b;
 box-shadow:inset 4px 4px 0 #9a9a9a,inset -4px -4px 0 #3e3e3e,0 0 0 4px #161616}
.hdr{position:absolute;left:60px;top:126px;font-family:P2;font-size:19px;letter-spacing:1px;padding:12px 16px;background:rgba(20,20,24,.82);
 box-shadow:0 0 0 4px #161616,inset 0 -4px 0 #000}
.hdr b{color:var(--y);font-weight:400}
.plogo{position:absolute;right:170px;top:104px;width:84px;filter:drop-shadow(4px 4px 0 rgba(0,0,0,.6))}
.k{position:absolute;left:62px;font-family:P2;font-size:20px;letter-spacing:1px;color:var(--y);text-shadow:3px 3px 0 #2a2a2a}
.big{position:absolute;left:58px;width:960px;font-family:PX;font-weight:700;line-height:.9;text-shadow:9px 9px 0 #2a2a2a}
.big em{font-style:normal;color:var(--g);text-shadow:9px 9px 0 #1d3b11}
.splash{position:absolute;font-family:P2;color:var(--y);text-shadow:5px 5px 0 #3f3a00;transform:rotate(-6deg);transform-origin:left center;white-space:nowrap}
.gui{position:absolute;background:var(--sl);color:#3a3a3a;box-shadow:inset 6px 6px 0 #fff,inset -6px -6px 0 #555,0 0 0 5px #000;padding:26px 28px}
.gui h3{font-family:P2;font-size:15px;color:#404040;margin-bottom:16px;letter-spacing:1px}
.row{display:flex;align-items:center;gap:16px;margin-top:8px}
.slot{width:54px;height:54px;flex:none;background:#8b8b8b;box-shadow:inset 4px 4px 0 #373737,inset -4px -4px 0 #fff;display:flex;align-items:center;justify-content:center;
 font-family:P2;font-size:24px;color:#fff;text-shadow:3px 3px 0 #3f3f3f}
.row span{font-family:PX;font-weight:700;font-size:29px;color:#2b2b2b;letter-spacing:.5px}
.swipe{position:absolute;left:62px;font-family:P2;font-size:18px;color:#fff;text-shadow:3px 3px 0 #000}
.swipe b{color:var(--y);font-weight:400}
.num{position:absolute;left:58px;font-family:P2;font-size:150px;line-height:1;color:var(--y);text-shadow:12px 12px 0 #5a4a00}
.num.r{left:auto;right:150px}
.shade.cv{background:linear-gradient(180deg,rgba(10,10,14,.82) 0%,rgba(10,10,14,.62) 40%,rgba(10,10,14,.8) 62%,rgba(10,10,14,.96) 100%)}
.panel{position:absolute;left:44px;width:888px;background:rgba(22,22,28,.9);box-shadow:0 0 0 5px #000,inset 0 0 0 4px #3b3b45;padding:30px 34px 34px}
.panel .kk{font-family:P2;font-size:17px;color:var(--g);letter-spacing:1px;margin-bottom:16px}
.panel .h{position:static;font-family:PX;font-weight:700;font-size:86px;line-height:.95;text-shadow:6px 6px 0 #000;margin-bottom:18px}
.panel .h em{font-style:normal;color:var(--y)}
.panel p{font-family:IT;font-weight:600;font-size:36px;line-height:1.32;color:#e9e9ee}
.panel p b{color:#fff;font-weight:800}.panel p .hl{color:var(--y);font-weight:800}
.facts{display:flex;gap:16px;margin-top:22px}
.facts div{flex:1;background:var(--sl);box-shadow:inset 4px 4px 0 #fff,inset -4px -4px 0 #555,0 0 0 4px #000;padding:14px 16px;color:#333}
.facts small{display:block;font-family:P2;font-size:12px;color:#555;margin-bottom:8px}
.facts strong{display:block;font-family:P2;font-size:30px;line-height:1.2;color:#2b2b2b}
.src{position:absolute;left:62px;bottom:134px;max-width:720px;font-family:IT;font-weight:600;font-size:17px;color:rgba(255,255,255,.55)}
.prog{position:absolute;right:160px;bottom:138px;display:flex;gap:8px}
.prog i{display:block;width:22px;height:10px;background:#555;box-shadow:0 0 0 3px #000}.prog i.on{background:var(--y)}
.btn{position:absolute;left:62px;font-family:PX;font-weight:700;font-size:64px;color:#fff;text-shadow:5px 5px 0 #1d3b11;padding:22px 40px;background:#2f7a1f;
 box-shadow:inset 6px 6px 0 #5aa83c,inset -6px -6px 0 #1b4a10,0 0 0 5px #000}
.btn small{display:block;font-family:P2;font-size:14px;color:#fff;text-shadow:2px 2px 0 #1d3b11;margin-bottom:10px}
.fol{position:absolute;left:62px;font-family:PX;font-weight:700;font-size:62px;text-shadow:6px 6px 0 #000}
.fol em{font-style:normal;color:var(--y)}
.disc{position:absolute;left:62px;top:1212px;font-family:P2;font-size:12px;line-height:1.9;color:rgba(255,255,255,.75);text-shadow:2px 2px 0 #000}
.cut{position:absolute;filter:drop-shadow(10px 10px 0 rgba(0,0,0,.45));image-rendering:pixelated}
"""


def base(body, d, bg=None, cover=False, idx=None, total=None):
    prog = ''
    if idx is not None and total:
        prog = '<div class="prog">' + ''.join(f'<i class="{"on" if i == idx else ""}"></i>' for i in range(total)) + '</div>'
    head = ('<div class="brand"><b>MINECRAFT</b><span class="tile">UNOFFICIAL<br>FAN GUIDE</span></div>' if cover else
            f'<div class="hdr">MINECRAFT · <b>{E(d.get("hdr", "TIPS"))}</b></div>')
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>'
            + (f'<div class="bg" style="background-image:url(/_build/mc/{bg})"></div>' if bg else '')
            + f'<div class="shade{" cv" if cover or d.get("_cta") else ""}"></div>' + body + head + '<img class="plogo" src="/assets/logo.png">' + prog
            + (f'<div class="src">{E(d["source"])}</div>' if d.get('source') and not cover else '')
            + R.FITJS + '</body></html>')


def cover(d):
    c = d['cover']
    cut = c.get('cutout')
    rows = ''.join(f'<div class="row"><div class="slot">{i + 1}</div><span>{E(t)}</span></div>' for i, t in enumerate(c.get('list', [])))
    body = ((f'<img class="cut" src="/_build/mc/{cut["img"]}" style="right:{cut.get("right", 40)}px;top:{cut.get("top", 760)}px;height:{cut.get("h", 560)}px">' if cut else '')
            + f'<div class="k" style="top:{c.get("kicker_top2", 300)}px">{E(c["kicker"])}</div>'
            + f'<div class="big fit" style="top:350px" data-size="{c.get("size", 168)}" data-max="960">{c["big"]}</div>'
            + (f'<div class="splash neon" style="left:70px;top:{c.get("splash_top", 690)}px;font-size:{c.get("splash_size", 40)}px">{E(c["splash"])}</div>' if c.get('splash') else '')
            + (f'<div class="gui" style="left:56px;top:{c.get("list_top", 790)}px;width:560px"><h3>{E(c.get("list_title", "INSIDE"))}</h3>{rows}</div>' if rows else '')
            + f'<div class="swipe" style="top:{c.get("swipe_top", 1250)}px">{c.get("swipe", "SWIPE FOR ALL <b>›</b>")}</div>')
    return base(body, d, bg=c.get('bg'), cover=True)


def tip(s, d, i, total):
    facts = ''
    if s.get('facts'):
        facts = '<div class="facts">' + ''.join(f'<div><small>{E(a)}</small><strong>{E(b)}</strong></div>' for a, b in s['facts']) + '</div>'
    top = s.get('panel_top', 700)
    body = (f'<div class="num{" r" if s.get("idx_right") else ""}" style="top:{top - 190}px">{i:02d}</div>'
            + f'<div class="panel" style="top:{top}px"><div class="kk">{E(s["kicker"])}</div>'
            + f'<div class="h fit" data-size="86" data-max="820">{s["title"]}</div><p>{s["body"]}</p>{facts}</div>')
    return base(body, d, bg=s.get('bg'), idx=i - 1, total=total)


def cta(d):
    c = d['cta']
    body = (f'<div class="big" style="top:260px;font-size:{c.get("size", 124)}px">{c["title"]}</div>'
            + f'<div class="splash neon" style="left:70px;top:590px;font-size:40px">{E(c["splash"])}</div>'
            + '<div class="k" style="top:690px;color:#fff">YOUR MINECRAFT CHEAT SHEET</div><div class="btn" style="top:735px">SAVE THIS</div>'
            + '<div class="fol" style="top:1000px">FOLLOW <em>@PLAYHQTV</em></div>'
            + f'<div class="disc">{DISC}</div>')
    return base(body, {**d, 'source': '', '_cta': 1}, bg=c.get('bg'))


# ---------- premium "ranked" layout (user 18.11.: "Optik muss besser und hochwertiger sein") ----------
# Own 3D voxel scenes from mc_scene.py as backgrounds, tier badge + segmented stat bars, dark glass panels.
CSS2 = """
.sh2{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,8,12,.9) 0%,rgba(8,8,12,.72) 24%,rgba(8,8,12,0) 37%,rgba(8,8,12,0) 54%,rgba(8,8,12,.82) 64%,rgba(8,8,12,.95) 100%)}
.sh2.cv{background:linear-gradient(180deg,rgba(8,8,12,.86) 0%,rgba(8,8,12,.7) 30%,rgba(8,8,12,.15) 47%,rgba(8,8,12,.1) 62%,rgba(8,8,12,.8) 76%,rgba(8,8,12,.95) 100%)}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 220px rgba(0,0,0,.55)}
.tb{position:absolute;left:58px;top:212px;width:136px;height:136px;display:flex;align-items:center;justify-content:center;font-family:PX;font-weight:700;font-size:118px;line-height:1;color:#fff;
 text-shadow:6px 6px 0 rgba(0,0,0,.45);box-shadow:inset 7px 7px 0 rgba(255,255,255,.35),inset -7px -7px 0 rgba(0,0,0,.35),0 0 0 6px #000,0 0 40px var(--a)}
.rk{position:absolute;left:226px;top:220px;font-family:P2;font-size:21px;letter-spacing:1px;color:var(--a);text-shadow:3px 3px 0 #000}
.rk b{display:inline-block;margin-left:12px;padding:6px 10px 5px;font-weight:400;font-size:15px;color:#111;background:var(--y);box-shadow:0 0 0 3px #000;vertical-align:3px;text-shadow:none}
.nm{position:absolute;left:222px;top:258px;width:800px;font-family:PX;font-weight:700;font-size:100px;line-height:.95;color:#fff;text-shadow:7px 7px 0 #000}
.st{position:absolute;left:44px;width:888px;background:linear-gradient(180deg,rgba(26,26,34,.94),rgba(14,14,20,.96));box-shadow:0 0 0 5px #000,inset 0 6px 0 var(--a),inset 0 0 0 3px rgba(255,255,255,.06);padding:34px 34px 30px}
.sr{display:flex;align-items:center;margin-bottom:16px}
.sr label{flex:none;width:205px;font-family:P2;font-size:17px;color:#cfcfd8;letter-spacing:1px}
.bar{display:flex;gap:5px;flex:none}
.bar i{display:block;width:18px;height:30px;background:#2b2b35;box-shadow:inset 0 -5px 0 rgba(0,0,0,.35)}
.bar i.f{background:var(--a);box-shadow:inset 0 5px 0 rgba(255,255,255,.45),inset 0 -5px 0 rgba(0,0,0,.3)}
.sr strong{margin-left:auto;white-space:nowrap;font-family:P2;font-weight:400;font-size:27px;line-height:1;color:#fff;text-shadow:3px 3px 0 #000}
.sr strong small{font-size:16px;color:#9a9aa8}
.vd{margin-top:6px;padding-top:18px;border-top:4px solid rgba(255,255,255,.08);font-family:IT;font-weight:600;font-size:33px;line-height:1.28;color:#e9e9ee}
.vd b{color:#fff;font-weight:800}.vd .hl{color:var(--y);font-weight:800}
.ttl{position:absolute;left:56px;width:968px;font-family:PX;font-weight:700;line-height:.9;text-shadow:9px 9px 0 #000}
.ttl em{font-style:normal;color:var(--y);text-shadow:9px 9px 0 #4a3a00}
.chips{position:absolute;left:58px;display:flex;gap:12px}
.chips span{font-family:P2;font-size:16px;color:#fff;padding:12px 14px 10px;background:rgba(18,18,24,.9);box-shadow:0 0 0 4px #000,inset 0 -4px 0 var(--c)}
"""

CSS3 = """
.sh3{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,8,12,.9) 0%,rgba(8,8,12,.55) 22%,rgba(8,8,12,0) 32%,rgba(8,8,12,0) 64%,rgba(8,8,12,.8) 71%,rgba(8,8,12,.96) 100%)}
.sh3.cv{background:linear-gradient(180deg,rgba(8,8,12,.9) 0%,rgba(8,8,12,.75) 30%,rgba(8,8,12,.1) 46%,rgba(8,8,12,0) 70%,rgba(8,8,12,.7) 84%,rgba(8,8,12,.92) 100%)}
.sh3.ct{background:linear-gradient(90deg,rgba(8,8,12,.9) 0%,rgba(8,8,12,.7) 45%,rgba(8,8,12,0) 68%),linear-gradient(180deg,rgba(8,8,12,.5) 0%,rgba(8,8,12,0) 30%,rgba(8,8,12,0) 75%,rgba(8,8,12,.8) 100%)}
.card{position:absolute;left:44px;width:888px;top:985px;background:rgba(14,14,20,.9);box-shadow:0 0 0 5px #000,inset 0 6px 0 var(--a);padding:30px 34px 28px}
.card .sr{margin-bottom:14px}
.card .vd{border:0;padding-top:6px;margin-top:4px;font-size:34px}
.src{bottom:158px}.prog{bottom:162px}
"""

TIERC = {'S': '#ff4d3d', 'A': '#ff9f1c', 'B': '#ffd23f', 'C': '#5ad16b', 'D': '#3aa7ff', 'F': '#8a8a96'}


def base2(body, d, bg, accent, cover=False, idx=None, total=None, cls='', v3=False):
    prog = ''
    if idx is not None and total:
        prog = '<div class="prog">' + ''.join(f'<i class="{"on" if i == idx else ""}"></i>' for i in range(total)) + '</div>'
    head = ('<div class="brand"><b>MINECRAFT</b><span class="tile">UNOFFICIAL<br>FAN GUIDE</span></div>' if cover else
            f'<div class="hdr">MINECRAFT · <b>{E(d.get("hdr", "TIPS"))}</b></div>')
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + CSS2 + (CSS3 if v3 else '') + f':root{{--a:{accent}}}</style></head><body>'
            + f'<div class="bg" style="background-image:url(/_build/mc/{bg});image-rendering:auto;top:{-28 if not (cover or v3) else 0}px;bottom:{28 if not (cover or v3) else 0}px"></div><div class="{'sh3' if v3 else 'sh2'} {cls}"></div><div class="vig"></div>'
            + body + head + '<img class="plogo" src="/assets/logo.png">' + prog
            + (f'<div class="src">{E(d["source"])}</div>' if d.get('source') and not cover else '')
            + R.FITJS + '</body></html>')


def bar(v, mx, n=20):
    f = round(v / mx * n) if v else 0
    if v and f == 0:
        f = 1
    return '<div class="bar">' + ''.join(f'<i class="{"f" if i < f else ""}"></i>' for i in range(n)) + '</div>'


def rank_cover(d):
    c = d['cover']
    if d.get('v3'):
        body = (f'<div class="k" style="top:{c.get("kicker_top", 300)}px">{E(c["kicker"])}</div>'
                + f'<div class="ttl fit" style="top:{c.get("title_top", 345)}px" data-size="{c.get("size", 120)}" data-max="968">{c["big"]}</div>'
                + f'<div class="splash neon" style="left:66px;top:{c.get("splash_top", 690)}px;font-size:{c.get("splash_size", 34)}px">{E(c["splash"])}</div>'
                + f'<div class="swipe" style="top:{c.get("swipe_top", 1235)}px">{c.get("swipe", "SWIPE FOR THE RANKING <b>›</b>")}</div>')
        return base2(body, d, c['bg'], '#ffe14d', cover=True, cls='cv', v3=True)
    chips = ''.join(f'<span style="--c:{TIERC[t]}"><b style="color:{TIERC[t]};font-weight:400">{E(t)}</b> {E(n)}</span>' for t, n in c.get('chips', []))
    body = (f'<div class="k" style="top:{c.get("kicker_top", 300)}px">{E(c["kicker"])}</div>'
            + f'<div class="ttl fit" style="top:{c.get("title_top", 345)}px" data-size="{c.get("size", 120)}" data-max="968">{c["big"]}</div>'
            + (f'<div class="splash neon" style="left:66px;top:{c.get("splash_top", 690)}px;font-size:{c.get("splash_size", 34)}px">{E(c["splash"])}</div>' if c.get('splash') else '')
            + (f'<div class="chips" style="top:{c.get("chips_top", 1110)}px">{chips}</div>' if chips else '')
            + f'<div class="swipe" style="top:{c.get("swipe_top", 1200)}px">{c.get("swipe", "SWIPE FOR THE RANKING <b>›</b>")}</div>')
    return base2(body, d, c['bg'], '#ffe14d', cover=True, cls='cv')


def rank_slide(s, d, i, total):
    a = s.get('accent', '#ffe14d')
    if d.get('v3'):
        rows = ''.join(f'<div class="sr"><label>{E(lb)}</label>{bar(v, mx)}<strong>{txt}</strong></div>' for lb, v, mx, txt in s['stats'][:2])
        body = (f'<div class="tb" style="background:{TIERC[s["tier"]]}">{E(s["tier"])}</div>'
                + f'<div class="rk">RANK #{s["rank"]} OF {d.get("of", 7)}{"<b>" + E(s["tag"]) + "</b>" if s.get("tag") else ""}</div>'
                + f'<div class="nm fit" data-size="100" data-max="800">{E(s["name"])}</div>'
                + f'<div class="card">{rows}<div class="vd">{s["verdict"]}</div></div>')
        return base2(body, d, s['bg'], a, idx=i - 1, total=total, v3=True)
    rows = ''.join(f'<div class="sr"><label>{E(lb)}</label>{bar(v, mx)}<strong>{txt}</strong></div>' for lb, v, mx, txt in s['stats'])
    body = (f'<div class="tb" style="background:{TIERC[s["tier"]]}">{E(s["tier"])}</div>'
            + f'<div class="rk">RANK #{s["rank"]} OF {d.get("of", 7)}{"<b>" + E(s["tag"]) + "</b>" if s.get("tag") else ""}</div>'
            + f'<div class="nm fit" data-size="100" data-max="800">{E(s["name"])}</div>'
            + f'<div class="st" style="top:{s.get("panel_top", 868)}px">{rows}<div class="vd">{s["verdict"]}</div></div>')
    return base2(body, d, s['bg'], a, idx=i - 1, total=total)


def rank_cta(d):
    c = d['cta']
    if d.get('v3'):
        body = (f'<div class="ttl" style="top:250px;font-size:{c.get("size", 100)}px;width:600px">{c["title"]}</div>'
                + f'<div class="splash neon" style="left:66px;top:{c.get("splash_top", 640)}px;font-size:32px">{E(c["splash"])}</div>'
                + '<div class="k" style="top:770px;color:#fff">YOUR ARMOR CHEAT SHEET</div><div class="btn" style="top:815px">SAVE THIS</div>'
                + '<div class="fol" style="top:1030px;font-size:56px">FOLLOW <em>@PLAYHQTV</em></div>'
                + f'<div class="disc" style="top:1130px;width:560px">{DISC.replace("<br>", " ")}</div>')
        return base2(body, {**d, 'source': ''}, c['bg'], '#ffe14d', cls='ct', v3=True)
    body = (f'<div class="ttl" style="top:250px;font-size:{c.get("size", 112)}px;width:640px">{c["title"]}</div>'
            + f'<div class="splash neon" style="left:66px;top:{c.get("splash_top", 640)}px;font-size:34px">{E(c["splash"])}</div>'
            + '<div class="k" style="top:745px;color:#fff">YOUR ARMOR CHEAT SHEET</div><div class="btn" style="top:790px">SAVE THIS</div>'
            + '<div class="fol" style="top:1030px">FOLLOW <em>@PLAYHQTV</em></div>'
            + f'<div class="disc" style="top:1150px">{DISC}</div>')
    return base2(body, {**d, 'source': ''}, c['bg'], '#ffe14d')


def main(data_path, out_dir):
    d = json.load(open(data_path))
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
    if d.get('ranks'):
        n = len(d['ranks'])
        pages = [('01_cover', rank_cover(d))] + [(f'{i + 2:02d}_slide', rank_slide(s, d, i + 1, n)) for i, s in enumerate(d['ranks'])]
        pages.append((f'{len(pages) + 1:02d}_cta', rank_cta(d)))
    else:
        n = len(d['tips'])
        pages = [('01_cover', cover(d))] + [(f'{i + 2:02d}_slide', tip(s, d, i + 1, n)) for i, s in enumerate(d['tips'])]
        pages.append((f'{len(pages) + 1:02d}_cta', cta(d)))
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=2)
        for nm, h in pages:
            open(os.path.join(tmp, nm + '.html'), 'w').write(h)
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/{nm}.html')
            pg.wait_for_selector('body[data-ready]'); pg.wait_for_timeout(400)
            raw = os.path.join(tmp, nm + '@2x.png'); pg.screenshot(path=raw, type='png')
            im = Image.open(raw).convert('RGB').resize((1080, 1440), Image.LANCZOS)  # no sharpening: keeps pixel edges clean
            R.save_jpg(im, os.path.join(out_dir, nm + '.jpg')); print(os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
