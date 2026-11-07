"""Animated PlayHQ logo for the video frame (user wish 04.11.2026).

The frame (frame.py) puts the static logo at x=916, y=176, 104 px. This script renders a seamless 6 s loop
(60 fps) of a 180x176 patch (x=880, y=140) = the band background + the logo with:
  - dashed gold ring turning once per 6 s
  - play triangle "beat" every 1.5 s (small scale pop + gold glow)
  - a light sheen sweeping across the logo once per loop
freeze.py overlays this loop on the whole video (also covers the old static logo).
Usage: python3 logo_anim.py <out.mp4>   (cached in _build/, not committed)
"""
import math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, '..', 'meta-carousel', 'assets', 'logo.png')
FPS, SECS = 60, 6
PATCH_XY, PATCH_WH = (880, 140), (180, 176)
LOGO_XY, LOGO_W = (36, 36), 104      # inside the patch
BG = (11, 11, 10)                    # band colour behind the logo (frame.py top band)
SS = 4                               # supersampling


def layers():
    lg = Image.open(LOGO).convert('RGBA')
    a = np.array(lg).astype(float)
    yy, xx = np.mgrid[0:1024, 0:1024]; r = np.hypot(xx - 512, yy - 512)
    yellow = (a[..., 0] > 180) & (a[..., 1] > 150) & (a[..., 2] < 90)
    ring_m = r > 455
    tri_m = (~ring_m) & yellow & (yy < 540)
    def sub(m):
        b = a.copy(); b[..., 3] *= m; return Image.fromarray(b.astype('uint8'))
    base = a.copy(); base[..., 3] *= ~(ring_m | tri_m)
    # fill the hole the ring leaves with the black disc so only the dashes move
    disc = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse((2, 2, 1022, 1022), fill=(14, 14, 14, 255))
    ys, xs = np.nonzero(tri_m); tc = (xs.mean(), ys.mean())
    return disc, Image.fromarray(base.astype('uint8')), sub(ring_m), sub(tri_m), tc


def frame(i, L, rgba=False):
    disc, base, ring, tri, tc = L
    t = i / FPS
    im = disc.copy()
    im.alpha_composite(ring.rotate(-360 * t / SECS, resample=Image.BICUBIC))
    im.alpha_composite(base)
    ph = (t % 1.5) / 1.5
    beat = math.exp(-ph * 7)                      # 1 at the beat, decays fast
    s = 1 + 0.07 * beat
    w = int(1024 * s); tr = tri.resize((w, w), Image.BICUBIC)
    ox, oy = int(tc[0] - tc[0] * s), int(tc[1] - tc[1] * s)
    glow = tr.filter(ImageFilter.GaussianBlur(45)); ga = glow.split()[3].point(lambda v: min(255, int(v * 2.2 * beat)))
    glow.putalpha(ga)
    layer = Image.new('RGBA', (1024, 1024)); layer.paste(glow, (ox, oy), glow)
    im.alpha_composite(layer)
    t2 = Image.new('RGBA', (1024, 1024)); t2.paste(tr, (ox, oy), tr); im.alpha_composite(t2)
    # sheen: diagonal light band once per loop (first 1.2 s)
    if t < 1.2:
        p = t / 1.2; sh = Image.new('L', (1024, 1024), 0); d = ImageDraw.Draw(sh)
        x0 = -400 + p * 1800
        d.polygon([(x0, 0), (x0 + 140, 0), (x0 - 260, 1024), (x0 - 400, 1024)], fill=70)
        sh = sh.filter(ImageFilter.GaussianBlur(30))
        sh = ImageChops.multiply(sh, im.split()[3])
        white = Image.new('RGBA', (1024, 1024), (255, 255, 255, 0)); white.putalpha(sh)
        im.alpha_composite(white)
    lg = im.resize((LOGO_W * SS, LOGO_W * SS), Image.LANCZOS)
    p = Image.new('RGBA', (PATCH_WH[0] * SS, PATCH_WH[1] * SS), (0, 0, 0, 0) if rgba else BG + (255,))
    p.alpha_composite(lg, (LOGO_XY[0] * SS, LOGO_XY[1] * SS))
    p = p.resize(PATCH_WH, Image.LANCZOS)
    return p if rgba else p.convert('RGB')


def build(out):
    L = layers()
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(FPS * SECS):
            frame(i, L).save(f'{tmp}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.png',
                        '-c:v', 'libx264', '-crf', '10', '-pix_fmt', 'yuv420p', out], check=True)
    return out


def get():
    p = os.path.join(HERE, '_build', 'logo_loop.mp4')
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True); build(p)
    return p


if __name__ == '__main__':
    print(build(sys.argv[1]))
