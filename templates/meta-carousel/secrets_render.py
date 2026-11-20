"""PlayHQ "map secrets" carousel (e.g. Warzone Zodiac secret challenges), design v3 HUD like the build posts.
Usage: python3 secrets_render.py data/<file>.json [out_dir]
Slides: cover (top rewards list), one slide per secret (steps + reward + stat), a 3-card "quick wins" slide,
a compact "grind" list slide, cta (render.cta_slide with the reward list). 1080x1440."""
import json, os, sys
import render as R
import build_render as B

E = R.E

CSS = """
.ic{width:96px;height:96px;flex:none;display:grid;place-items:center;border:2px solid rgba(245,196,0,.35);background:rgba(245,196,0,.06)}
.rq{position:absolute;left:50px;right:145px;height:150px;display:flex;align-items:center;gap:26px;padding:0 26px}
.rq b{display:block;font-family:Anton;font-size:40px;line-height:1.05;letter-spacing:1px;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.rq span{display:block;font-weight:700;font-size:19px;letter-spacing:5px;color:#bdbdbd;margin-top:6px}
.rq p{margin:8px 0 0;font-weight:600;font-size:27px;line-height:1.15;color:#f1f1f1}
.rq p em{font-style:normal;color:var(--y);font-weight:700}
.rg{position:absolute;left:50px;right:145px;height:112px;display:flex;align-items:center;gap:22px;padding:0 22px}
.rg .ic{width:76px;height:76px}
.rg b{display:block;font-weight:700;font-size:28px;letter-spacing:1px;line-height:1.05;color:var(--y)}
.rg p{margin:6px 0 0;font-weight:600;font-size:24px;color:#e6e6e6}
.rg .cnt{margin-left:auto;font-family:Anton;font-size:44px;text-align:right;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.rg .cnt small{display:block;font-family:Raj;font-size:14px;font-weight:700;letter-spacing:3px;-webkit-text-fill-color:#bdbdbd}

.cstep{position:absolute;left:60px;right:150px;display:flex;align-items:center;gap:28px}
.cstep .sn{font-family:Anton;font-size:64px;width:70px;flex:none;text-align:center;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.cstep b{font-weight:600;font-size:40px;line-height:1.12;color:#f1f1f1}
.cstep b em{font-style:normal;color:var(--y);font-weight:700}
.pill{position:absolute;left:60px;height:84px;display:flex;align-items:center;padding:0 30px;gap:18px}
.pill small{font-weight:700;font-size:20px;letter-spacing:6px;color:#3a2a00}
.pill b{font-family:Anton;font-size:46px;color:#140f00;letter-spacing:1px}

.step{position:absolute;left:50px;right:145px;height:88px;display:flex;align-items:center;gap:22px;padding:0 24px}
.step .sn{font-family:Anton;font-size:48px;width:56px;text-align:center;flex:none;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.step b{font-weight:600;font-size:30px;line-height:1.12;letter-spacing:.5px;color:#f1f1f1}
.step b em{font-style:normal;color:var(--y);font-weight:700}
.rw{position:absolute;left:50px;right:145px;height:112px;display:flex;align-items:center;padding:0 28px;gap:24px}
.rw small{display:block;font-weight:700;font-size:18px;letter-spacing:6px;color:#3a2a00}
.rw b{display:block;font-family:Anton;font-size:44px;line-height:1.05;color:#140f00;letter-spacing:1px}
.stat{position:absolute;right:150px;text-align:right}
.stat strong{display:block;font-family:Anton;font-size:84px;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.stat small{display:block;font-size:22px;letter-spacing:6px;color:#bdbdbd;font-weight:700;margin-top:6px}
.where{position:absolute;left:60px;font-weight:700;font-size:26px;letter-spacing:6px;color:#cfcfcf;display:flex;align-items:center;gap:14px}
.where i{display:block;width:44px;height:5px;background:var(--y)}
.where b{color:var(--y)}
.tip{position:absolute;left:50px;right:145px;font-weight:600;font-size:26px;letter-spacing:1px;color:#cfcfcf;padding-left:22px;border-left:4px solid var(--y)}
.tip b{color:var(--y);letter-spacing:4px;font-size:22px;margin-right:12px}
.qc{position:absolute;left:50px;right:145px;height:232px;padding:20px 30px}
.qc .qt{font-family:Anton;font-size:52px;line-height:1;letter-spacing:2px}
.qc .qw{font-weight:700;font-size:20px;letter-spacing:6px;color:#bdbdbd;margin-top:10px}
.qc .qh{font-weight:600;font-size:29px;line-height:1.15;color:#f1f1f1;margin-top:16px;max-width:820px}
.qc .qh em,.tip em{font-style:normal;color:var(--y);font-weight:700}
.rw .rt{margin-left:auto;max-width:400px;font-weight:700;font-size:21px;line-height:1.2;color:#2a1f00;text-align:right}
.rw .rt span{display:block;font-size:16px;letter-spacing:5px;color:#140f00;margin-bottom:4px}
.bigstat{position:absolute;left:0;right:90px;text-align:center}
.bigstat strong{display:block;font-family:Anton;font-size:190px;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.bigstat small{display:block;font-size:30px;letter-spacing:12px;color:#d9d9d9;font-weight:700;margin-top:6px}
.qc .qr{position:absolute;left:30px;bottom:24px;font-weight:700;font-size:22px;letter-spacing:4px;color:var(--y)}
.qc .qn{position:absolute;right:26px;top:22px;font-family:Anton;font-size:40px;color:rgba(255,212,0,.35)}
.gl{position:absolute;left:50px;right:145px;height:118px;padding:0 26px;display:flex;align-items:center;gap:22px}
.gl .gx{font-family:Anton;font-size:46px;width:120px;flex:none;text-align:center;line-height:1;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.gl .gx small{display:block;font-family:Raj;font-weight:700;font-size:15px;letter-spacing:3px;-webkit-text-fill-color:#bdbdbd;margin-top:4px}
.gl b{display:block;font-weight:700;font-size:30px;letter-spacing:1px;line-height:1.05}
.gl span{display:block;font-weight:700;font-size:19px;letter-spacing:4px;color:var(--y);margin-top:6px}
.rrow{position:absolute;left:50px;right:150px;height:96px;display:flex;align-items:center;gap:22px;padding:0 26px}
.rrow .n{font-family:Anton;font-size:52px;width:60px;text-align:center;background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent}
.rrow .im{width:170px;height:76px;display:grid;place-items:center;flex:none}
.rrow .im img{max-width:170px;max-height:70px;filter:drop-shadow(0 10px 8px rgba(0,0,0,.8)) brightness(1.2)}
.rrow .im i{font-style:normal;font-family:Anton;font-size:40px;color:var(--y)}
.rrow b{font-weight:700;font-size:30px;letter-spacing:2px;line-height:1.05}
.rrow small{display:block;font-weight:700;font-size:19px;letter-spacing:4px;color:var(--y);margin-top:4px}
"""


ICONS = {  # own simple line icons per reward type (no game artwork)
 'card': '<rect x="6" y="18" width="52" height="28" rx="3"/><path d="M12 38h22M12 30h14"/><circle cx="48" cy="32" r="6"/>',
 'emblem': '<path d="M32 6l22 8v16c0 14-10 23-22 28C20 53 10 44 10 30V14z"/><path d="M24 31l6 6 11-12"/>',
 'sticker': '<path d="M10 10h44v30L40 54H10z"/><path d="M54 40H40v14"/>',
 'decal': '<path d="M32 6l26 26-26 26L6 32z"/><path d="M32 18l14 14-14 14-14-14z"/>',
 'contrail': '<path d="M8 50c14 0 18-12 26-20S50 14 58 14"/><path d="M8 40c10 0 14-8 20-14"/><circle cx="56" cy="14" r="3"/>',
 'charm': '<circle cx="20" cy="16" r="9"/><path d="M27 22l8 8"/><rect x="32" y="27" width="20" height="30" rx="4"/><path d="M38 50h8"/>',
 'parachute': '<path d="M6 30C6 14 18 6 32 6s26 8 26 24"/><path d="M6 30l26 24 26-24M19 30l13 24 13-24M32 30v24"/>',
 'screen': '<rect x="6" y="10" width="52" height="34" rx="3"/><path d="M24 54h16M32 44v10"/><path d="M14 36l10-12 8 8 6-6 12 10"/>',
 'camo': '<rect x="8" y="8" width="48" height="48" rx="6"/><path d="M8 26c10 4 16-6 26-2s12 10 22 6M8 42c8-4 14 4 24 0s14-8 24-4"/>',
}


def icon(k, size=72):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="#f5c400" stroke-width="3.2" '
            f'stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 8px rgba(245,196,0,.35))">{ICONS[k]}</svg>')


def page(body, d):
    return R.page(f'<style>{CSS}</style>' + body, d)


def head(top_white, top_gold, kicker, where):
    return (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(kicker)}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="700"><span class="gr w">{E(top_white)}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="700"><span class="gr gold">{E(top_gold)}</span></div>'
            + f'<div class="where" style="top:505px"><i></i>WHERE: <b>{E(where)}</b></div>')


def em(s):
    """*word* -> highlighted (escape first, then mark)."""
    out, on = '', False
    for part in E(s).split('*'):
        out += part if not on else f'<em>{part}</em>'
        on = not on
    return out


def secret_slide(s, d):
    n = len(s['steps'])
    top = s.get('steps_top', 770 if n >= 4 else 830)
    steps = ''.join(f'<div class="step hud" style="top:{top + i * 98}px"><div class="sn">{i + 1}</div><b>{em(t)}</b></div>'
                    for i, t in enumerate(s['steps']))
    y_rw = top + n * 98 + 8
    if s.get('image'):
        visual = (R.gun_html(s['image'], s.get('brightness', 1.2), 'edge', top=545, height=200, maxh=180)
                  + ('<div style="position:absolute;left:0;right:0;top:742px;text-align:center;font-weight:700;font-size:15px;letter-spacing:5px;color:#8a8a8a">BASE WEAPON SHOWN</div>' if s.get('base_note', 1) else ''))
        stat = f'<div class="stat" style="top:250px"><strong>{E(s["stat"])}</strong><small>{E(s["stat_label"])}</small></div>'
    else:  # no weapon: the stat becomes the hero visual
        visual = f'<div class="bigstat" style="top:{s.get("bigstat_top", 575)}px"><strong>{E(s["stat"])}</strong><small>{E(s["stat_label"])}</small></div>'
        stat = ''
    tip = f'<div class="rt"><span>TIP</span>{E(s["tip"])}</div>' if s.get('tip') else ''
    body = (head(s['title_white'], s['title_gold'], s['kicker'], s['where']) + stat + visual + steps
            + f'<div class="rw hud save" style="top:{y_rw}px"><div><small>REWARD</small><b>{E(s["reward"])}</b></div>{tip}</div>')
    return page(body, {**d, 'footer': ''})


def v2_slide(s, d):
    """Reward-first logic (user 20.11.): title, REWARD pill, where, picture, steps, tip."""
    n = len(s['steps'])
    top = 850 if n >= 4 else 900
    steps = ''.join(f'<div class="step hud" style="top:{top + i * 98}px"><div class="sn">{i + 1}</div><b>{em(t)}</b></div>'
                    for i, t in enumerate(s['steps']))
    if s.get('image'):
        visual = (R.gun_html(s['image'], s.get('brightness', 1.2), 'edge', top=640, height=175, maxh=158)
                  + '<div style="position:absolute;left:0;right:90px;top:828px;text-align:center;font-weight:700;font-size:15px;letter-spacing:5px;color:#8a8a8a">BASE WEAPON SHOWN</div>')
    else:
        visual = f'<div class="bigstat" style="top:660px"><strong style="font-size:130px">{E(s["stat"])}</strong><small>{E(s["stat_label"])}</small></div>'
    y_tip = top + n * 98 + 14
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(s["kicker"])}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="860"><span class="gr w">{E(s["title_white"])}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="860"><span class="gr gold">{E(s["title_gold"])}</span></div>'
            + f'<div class="pill hud save" style="top:500px"><small>REWARD</small><b>{E(s["reward"])}</b></div>'
            + f'<div class="where" style="top:604px"><i></i>WHERE: <b>{E(s["where"])}</b></div>'
            + visual + steps
            + (f'<div class="tip" style="top:{y_tip}px"><b>TIP</b>{E(s["tip"])}</div>' if s.get('tip') else ''))
    return page(body, {**d, 'footer': ''})


def v2_quick(q, d):
    rows = ''.join(
        f'<div class="rq hud" style="top:{575 + i * 190}px"><div class="ic">{icon(c["icon"])}</div><div>'
        f'<b>{E(c["reward"])}</b><span>{E(c["where"])}</span><p>{em(c["how"])}</p></div></div>' for i, c in enumerate(q['cards']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(q["kicker"])}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="860"><span class="gr w">{E(q["title_white"])}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="860"><span class="gr gold">{E(q["title_gold"])}</span></div>'
            + f'<div class="where" style="top:505px"><i></i>{E(q["sub"])}</div>' + rows)
    return page(body, {**d, 'footer': ''})


def v2_grind(g, d):
    rows = ''.join(
        f'<div class="rg hud" style="top:{555 + i * 122}px"><div class="ic">{icon(r["icon"], 56)}</div><div>'
        f'<b>{E(r["reward"])}</b><p>{E(r["how"])}</p></div><div class="cnt">{E(r["x"])}<small>{E(r["unit"])}</small></div></div>'
        for i, r in enumerate(g['rows']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(g["kicker"])}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="860"><span class="gr w">{E(g["title_white"])}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="860"><span class="gr gold">{E(g["title_gold"])}</span></div>'
            + f'<div class="where" style="top:505px"><i></i>{E(g["sub"])}</div>' + rows)
    return page(body, {**d, 'footer': ''})


def clean_slide(s, d):
    """Simple layout (user 19.11.: 'zu unübersichtlich'): kicker, big name, reward pill, weapon or big stat, 3 short steps."""
    steps = ''.join(f'<div class="cstep" style="top:{900 + i * 118}px"><div class="sn">{i + 1}</div><b>{em(t)}</b></div>'
                    for i, t in enumerate(s['steps'][:3]))
    if s.get('image'):
        visual = (R.gun_html(s['image'], s.get('brightness', 1.2), 'edge', top=560, height=300, maxh=270)
                  + '<div style="position:absolute;left:0;right:90px;top:850px;text-align:center;font-weight:700;font-size:15px;letter-spacing:5px;color:#8a8a8a">BASE WEAPON SHOWN</div>')
    else:
        visual = f'<div class="bigstat" style="top:585px"><strong>{E(s["stat"])}</strong><small>{E(s["stat_label"])}</small></div>'
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px;letter-spacing:12px">{E(s["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="150" data-max="860"><span class="gr gold">{E(s["name"])}</span></div>'
            + f'<div class="pill hud save" style="top:430px"><small>REWARD</small><b>{E(s["reward"])}</b></div>'
            + visual + '<div class="line" style="top:878px"></div>' + steps)
    return page(body, {**d, 'footer': ''})


def clean_cover(d):
    c = d['cover']
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:28px;letter-spacing:12px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:245px" data-size="220" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:480px" data-size="140" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:640px;left:62px;font-size:30px;letter-spacing:8px;color:#d9d9d9">{E(c["sub"])}</div>'
            + '<div class="floor" style="top:1080px"></div><div class="line" style="top:1097px"></div>'
            + R.gun_html(c['image'], 1.2, 'edge', top=720, height=380, maxh=340)
            + f'<div class="swipe" style="top:1170px;font-size:28px;right:110px">{E(c["swipe"])}</div>')
    return R.page(f'<style>{CSS}</style>' + body, {**d, 'footer': ''})


def quick_slide(q, d):
    cards = ''.join(
        f'<div class="qc hud" style="top:{q.get("top", 562) + i * 248}px"><div class="qn">{i + 1:02d}</div><div class="qt"><span class="gr gold">{E(c["name"])}</span></div>'
        f'<div class="qw">WHERE: {E(c["where"])}</div><div class="qh">{em(c["how"])}</div><div class="qr">REWARD: {E(c["reward"])}</div></div>'
        for i, c in enumerate(q['cards']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(q["kicker"])}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="860"><span class="gr w">{E(q["title_white"])}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="860"><span class="gr gold">{E(q["title_gold"])}</span></div>'
            + f'<div class="where" style="top:505px"><i></i>{E(q["sub"])}</div>' + cards)
    return page(body, {**d, 'footer': ''})


def grind_slide(g, d):
    rows = ''.join(
        f'<div class="gl hud" style="top:{g.get("top", 560) + i * 126}px"><div class="gx">{E(r["x"])}<small>{E(r["unit"])}</small></div>'
        f'<div><b>{E(r["how"])}</b><span>{E(r["reward"])}</span></div></div>' for i, r in enumerate(g['rows']))
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(g["kicker"])}</div>'
            + f'<div class="fit" style="top:242px" data-size="118" data-max="860"><span class="gr w">{E(g["title_white"])}</span></div>'
            + f'<div class="fit" style="top:368px" data-size="118" data-max="860"><span class="gr gold">{E(g["title_gold"])}</span></div>'
            + f'<div class="where" style="top:505px"><i></i>{E(g["sub"])}</div>' + rows)
    return page(body, {**d, 'footer': ''})


def reward_rows(items, top, gap=110):
    return ''.join(
        f'<div class="rrow hud" style="top:{top + i * gap}px"><div class="n">{i + 1}</div><div class="im">'
        + (f'<img src="/weapons/{r["image"]}">' if r.get('image') else (icon(r['svg'], 64) if r.get('svg') else f'<i>{E(r.get("icon", "★"))}</i>'))
        + f'</div><div><b>{E(r["name"])}</b><small>{E(r["type"])}</small></div></div>' for i, r in enumerate(items))


def cover_slide(d):
    c = d['cover']
    body = (f'<div class="kicker" style="top:200px;left:60px;font-size:26px;letter-spacing:10px">{E(c["kicker"])}</div>'
            + f'<div class="fit" style="top:240px" data-size="190" data-max="860"><span class="gr gold">{E(c["big"])}</span></div>'
            + f'<div class="fit" style="top:440px" data-size="112" data-max="860"><span class="gr w">{E(c["small"])}</span></div>'
            + f'<div class="kicker" style="top:568px;left:62px;font-size:24px;letter-spacing:6px;color:#d9d9d9">{E(c["sub"])}</div>'
            + reward_rows(d['top_rewards'], 650)
            + f'<div class="swipe" style="top:{c.get("swipe_top", 1222)}px;font-size:26px;right:110px">{E(c["swipe"])}</div>')
    return R.page(f'<style>{CSS}</style>' + body, {**d, 'footer': ''})


def cta_slide(d):
    c = d['cta']
    body = (f'<div class="fit" style="top:205px" data-size="132" data-max="860"><span class="gr w">{E(c["white"])}</span></div>'
            + f'<div class="fit" style="top:350px" data-size="132" data-max="860"><span class="gr gold">{E(c["gold"])}</span></div>'
            + f'<div class="kicker" style="top:505px;left:60px;font-size:26px;letter-spacing:7px;color:#d9d9d9">{E(c["sub"])}</div>'
            + reward_rows(d['top_rewards'], 565, 104))
    y = c.get('follow_top', 1045)
    body = (R.cutout_html(c['cutout']) if c.get('cutout') else '') + body + (
        f'<img src="/assets/logo.png" style="position:absolute;left:60px;top:{y}px;width:110px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.7))">'
        f'<div style="position:absolute;left:190px;top:{y + 14}px;font-family:Anton;font-size:58px;line-height:1;letter-spacing:3px">FOLLOW <span style="background:linear-gradient(170deg,var(--g1),var(--g2) 45%,var(--g3));-webkit-background-clip:text;color:transparent">@PLAYHQTV</span></div>'
        f'<div style="position:absolute;left:192px;top:{y + 84}px;font-weight:700;color:#cfcfcf;letter-spacing:6px;font-size:21px">{E(c.get("follow_sub", "FOR DAILY WARZONE TIPS"))}</div>')
    return R.page(f'<style>{CSS}</style>' + body, {**d, 'footer': ''})


def main(data_path, out_dir=None):
    d = json.load(open(data_path))
    lay = d.get('layout')
    pages = [('01_cover', clean_cover(d) if lay == 'clean' else cover_slide(d))]
    for s in d['secrets']:
        f = {'clean': clean_slide, 'v2': v2_slide}.get(lay, secret_slide)
        pages.append((f'{len(pages) + 1:02d}_secret', f(s, d)))
    if d.get('quick'):
        pages.append((f'{len(pages) + 1:02d}_quick', (v2_quick if lay == 'v2' else quick_slide)(d['quick'], d)))
    if d.get('grind'):
        pages.append((f'{len(pages) + 1:02d}_grind', (v2_grind if lay == 'v2' else grind_slide)(d['grind'], d)))
    pages.append((f'{len(pages) + 1:02d}_cta', cta_slide(d)))
    B.render_pages(pages, data_path, out_dir) if hasattr(B, 'render_pages') else render_pages(pages, data_path, out_dir)


def render_pages(pages, data_path, out_dir=None):
    out_dir = out_dir or os.path.join(R.HERE, 'out', os.path.splitext(os.path.basename(data_path))[0])
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(R.HERE, '_build'); os.makedirs(tmp, exist_ok=True)
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
            print(os.path.join(out_dir, nm + '.jpg'))
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
