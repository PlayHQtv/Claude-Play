# Renders the PlayHQ 'Meta Builds' carousel slides to PNG with headless Chromium.
# Usage: python3 render.py   (edit DATA / ORDER / templates for a new carousel)
import re, sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SRC = HERE / 'templates'          # .dc.html slide templates (same files as the Claude Design canvas)
OUT = HERE / 'out'                # rendered PNGs land here (1080x1920)
OUT.mkdir(exist_ok=True)
W = 'file://' + str(HERE / 'weapons') + '/'
# Canvas asset ids -> local weapon screenshots (black background, side view)
BLOBS = {
    '/_blob/475d54e47f2bc410e3a17021df3bf343': W + 'hyeon-burst.png',
    '/_blob/6604d33538c2699e263c0d83bb5b7edd': W + 'han-86.png',
    '/_blob/cf8f920c3df230f3b13f02470ce6e56e': W + 'kastov-762.png',
    '/_blob/6db8aff92e5da3841c3528195f23f6b9': W + 'iso-nightshade.png',
}
I = {
 'BARREL': 'M4 21 H38 V27 H4 Z M38 23 H44 M10 21 V27',
 'MUZZLE': 'M8 16 H34 V32 H8 Z M15 16 V32 M22 16 V32 M34 21 H42 V27 H34',
 'OPTIC': 'M24 10 A14 14 0 1 0 24.01 10 Z M24 4 V14 M24 34 V44 M4 24 H14 M34 24 H44',
 'UNDERBARREL': 'M8 14 H40 L31 22 L27 38 H18 L21 22 Z',
 'REAR GRIP': 'M16 8 H32 L30 40 H18 Z M18 16 H30 M18 24 H30',
 'STOCK': 'M6 18 H30 L42 12 V36 L30 30 H6 Z',
 'MAGAZINE': 'M18 6 H30 L33 42 H21 Z M19 14 H31',
 'AMMO': 'M10 40 V20 L13 12 L16 20 V40 Z M21 40 V20 L24 12 L27 20 V40 Z M32 40 V20 L35 12 L38 20 V40 Z',
 'APEX': 'M24 6 L40 24 L24 42 L8 24 Z M24 15 L31 24 L24 33 L17 24 Z',
}
def parts(lst):
    return [{'slot': s, 'name': n, 'd': I[s]} for s, n in lst]
DATA = {
 'Main': {'guns': [
   {'n': '1', 'name': 'HYEON BURST', 'src': '/_blob/475d54e47f2bc410e3a17021df3bf343', 'b': 'lighten', 'f': 'none', 'c': '55', 'mask': 'radial-gradient(ellipse 80% 22% at 50% 55%, #000 70%, transparent 100%)'},
   {'n': '2', 'name': 'HAN 86', 'src': '/_blob/6604d33538c2699e263c0d83bb5b7edd', 'b': 'lighten', 'f': 'none', 'c': '47', 'mask': 'radial-gradient(ellipse 82% 75% at 50% 47%, #000 62%, transparent 100%)'},
   {'n': '3', 'name': 'KASTOV 762', 'src': '/_blob/cf8f920c3df230f3b13f02470ce6e56e', 'b': 'lighten', 'f': 'none', 'c': '59', 'mask': 'radial-gradient(ellipse 80% 22% at 50% 59%, #000 70%, transparent 100%)'},
   {'n': '4', 'name': 'ISO NIGHTSHADE', 'src': '/_blob/6db8aff92e5da3841c3528195f23f6b9', 'b': 'lighten', 'f': 'none', 'c': '55', 'mask': 'radial-gradient(ellipse 80% 34% at 50% 55%, #000 70%, transparent 100%)'}]},
 'Hyeon': {'parts': parts([('BARREL','MUGI SEUNGRI-0'),('MUZZLE','TZL-110 V1'),('UNDERBARREL','FSS FIRELINE G'),('APEX','APEX UNDERBARREL'),('AMMO','6.8X43MM HIGH')])},
 'Han86': {'parts': parts([('BARREL','SA H86 465MM'),('MUZZLE','ZLR REVERB90'),('OPTIC','ZLR TYPE C'),('UNDERBARREL','FSS TAC90 GRIP'),('REAR GRIP','XRK JUSTICE II')])},
 'Kastov': {'parts': parts([('BARREL','HAEBANG MT-414MM'),('MUZZLE','EXP R3000-V'),('OPTIC','FJX 708 PRO'),('UNDERBARREL','FSS TAC90 GRIP'),('REAR GRIP','FJX KASTOV GRIP')])},
 'Iso': {'parts': parts([('BARREL','ZLR MAG-Z 9'),('MUZZLE','XRK HERDER 40'),('STOCK','EXP G2-44 STOCK'),('UNDERBARREL','FSS FIRELINE GRIP'),('MAGAZINE','40 ROUND MAG')])},
 'Cta': {'picks': [{'n': '1', 'name': 'HYEON BURST'}, {'n': '2', 'name': 'HAN 86'}, {'n': '3', 'name': 'KASTOV 762'}, {'n': '4', 'name': 'ISO NIGHTSHADE'}]},
}
ORDER = ['Main', 'Hyeon', 'Han86', 'Kastov', 'Iso', 'Cta']

def build(name):
    s = (SRC / f'{name}.dc.html').read_text()
    s = re.sub(r'<script type="text/x-dc".*?</script>', '', s, flags=re.S)
    s = s.replace('<script src="./support.js"></script>', '')
    s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis[^>]*>', '', s)
    s = s.replace('<helmet>', '').replace('</helmet>', '').replace('<x-dc>', '').replace('</x-dc>', '')
    data = DATA[name]
    def loop(m):
        lst, var, body = m.group(1), m.group(2), m.group(3)
        out = []
        for it in data[lst]:
            b = body
            for k, v in it.items():
                b = b.replace('{{' + var + '.' + k + '}}', v)
            out.append(b)
        return ''.join(out)
    s = re.sub(r'<sc-for list="\{\{(\w+)\}\}" as="(\w+)"[^>]*>(.*?)</sc-for>', loop, s, flags=re.S)
    s = s.replace('{{accent}}', '#e8c25a')
    for k, v in BLOBS.items():
        s = s.replace(k, v)
    s = s.replace('Anton, Impact, sans-serif', "'Inter Display', Inter, sans-serif; font-weight: 900; letter-spacing: -1px")
    s = s.replace('Oswald, Arial, sans-serif', "Inter, sans-serif")
    assert '{{' not in s, (name, s[s.index('{{')-80:s.index('{{')+80])
    return s

FIT = """
() => {
  const els=[...document.querySelectorAll('div,span')].filter(e=>getComputedStyle(e).fontFamily.includes('Inter Display'));
  for (const e of els) { e.style.whiteSpace='nowrap'; }
  for (const e of els) {
    const p=e.parentElement; let fs=parseFloat(getComputedStyle(e).fontSize); let n=0;
    while ((e.scrollWidth>p.clientWidth+1 || e.getBoundingClientRect().width>p.getBoundingClientRect().width+1) && n<80) { fs-=2; e.style.fontSize=fs+'px'; n++; }
  }
  const tiles=[...document.querySelectorAll('span')].filter(e=>e.children.length===0 && parseFloat(getComputedStyle(e).fontSize)>=30);
  for (const e of tiles) { e.style.whiteSpace='nowrap'; let fs=parseFloat(getComputedStyle(e).fontSize); let n=0; const p=e.parentElement; while (p && e.scrollWidth>p.clientWidth && n<40){fs-=1;e.style.fontSize=fs+'px';n++;} }
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    for i, name in enumerate(ORDER, 1):
        f = OUT / f'{name}.html'
        f.write_text(build(name))
        pg.goto('file://' + str(f))
        pg.wait_for_timeout(400)
        pg.evaluate(FIT)
        pg.wait_for_timeout(150)
        pg.screenshot(path=str(OUT / f'slide{i}_{name}.png'), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
        print('ok', name)
    b.close()
