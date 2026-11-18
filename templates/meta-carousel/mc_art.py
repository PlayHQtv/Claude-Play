"""Original blocky pixel-art backdrops for the Minecraft-style template (own art, no Mojang textures/characters).
Writes _build/mc/scene_<name>.png. Usage: python3 mc_art.py"""
import os, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_build', 'mc'); os.makedirs(OUT, exist_ok=True)
P = 8          # texture pixels per block side
B = 60         # block size on screen (px)


def tex(base, var, seed, specks=None):
    r = random.Random(seed); im = Image.new('RGB', (P, P))
    for y in range(P):
        for x in range(P):
            k = r.uniform(-var, var); c = tuple(max(0, min(255, int(v * (1 + k)))) for v in base)
            if specks and r.random() < specks[1]: c = specks[0]
            im.putpixel((x, y), c)
    return im.resize((B, B), Image.NEAREST)


def grass(seed):
    im = tex((134, 96, 67), .14, seed); top = tex((98, 168, 66), .16, seed + 1)
    r = random.Random(seed); d = ImageDraw.Draw(im)
    im.paste(top.crop((0, 0, B, B * 3 // 8)), (0, 0))
    for x in range(P):  # ragged grass edge
        h = r.randint(3, 4) * B // P
        d.rectangle([x * B // P, 0, (x + 1) * B // P - 1, h], fill=tuple(int(v * r.uniform(.85, 1.1)) for v in (98, 168, 66)))
    return im


def scene(name, kind, seed=7, w=1080, h=1440):
    r = random.Random(seed); im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    if kind == 'day':
        for y in range(h): d.line([(0, y), (w, y)], fill=(int(120 + 60 * y / h), int(170 + 50 * y / h), 255))
        d.rectangle([760, 150, 880, 270], fill=(255, 236, 140))                                   # square sun
        for cx, cy, cw in ((80, 260, 5), (420, 200, 4), (620, 330, 6)):                          # blocky clouds
            for i in range(cw):
                d.rectangle([cx + i * 40, cy, cx + i * 40 + 39, cy + 40], fill=(250, 252, 255))
            d.rectangle([cx + 40, cy - 40, cx + (cw - 1) * 40 - 1, cy - 1], fill=(250, 252, 255))
        ground = [8 + int(2.2 * __import__('math').sin(i / 2.3 + seed)) for i in range(w // B + 1)]
    else:  # cave
        for y in range(h): d.line([(0, y), (w, y)], fill=(18 + y // 90, 20 + y // 90, 28 + y // 80))
        ground = [r.randint(14, 17) for _ in range(w // B + 1)]
    for i, gy in enumerate(ground):
        x = i * B
        for row in range(gy, h // B + 2):
            y = row * B
            if kind == 'day':
                t = grass(seed * 100 + i) if row == gy else tex((134, 96, 67), .14, row * 31 + i) if row < gy + 3 else \
                    tex((122, 122, 122), .18, row * 17 + i, ((40, 40, 40), .05) if r.random() < .15 else None)
            else:
                gem = ((70, 230, 220), .14) if r.random() < .06 else ((210, 150, 60), .1) if r.random() < .05 else None
                t = tex((86, 86, 92), .2, row * 13 + i * 7, gem)
            im.paste(t, (x, y))
        if kind == 'day' and r.random() < .18 and 2 < i < w // B - 3:                           # blocky tree
            top = (gy - 4) * B
            for k in range(4): im.paste(tex((104, 78, 46), .12, i + k), (x, top + k * B))
            for lx in range(-2, 3):
                for ly in range(-3, 0):
                    if abs(lx) == 2 and ly == -3: continue
                    im.paste(tex((58, 128, 46), .2, i * 7 + lx * 3 + ly), (x + lx * B, top + ly * B))
        if kind == 'cave':  # cave ceiling
            for row in range(0, r.randint(3, 5)):
                im.paste(tex((86, 86, 92), .2, row * 5 + i), (x, row * B))
    if kind == 'cave':  # torch glow
        for cx, cy in ((260, 760), (820, 690)):
            for rr in range(260, 0, -20):
                ov = Image.new('RGB', (w, h)); ImageDraw.Draw(ov).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 170, 60))
                im = Image.blend(im, Image.composite(ov, im, ov.convert('L').point(lambda v: 255 if v else 0)), .045)
            d = ImageDraw.Draw(im); d.rectangle([cx - 6, cy, cx + 6, cy + 50], fill=(110, 80, 40)); d.rectangle([cx - 8, cy - 18, cx + 8, cy], fill=(255, 210, 90))
    im.save(os.path.join(OUT, f'scene_{name}.png'))
    print(os.path.join(OUT, f'scene_{name}.png'))


if __name__ == '__main__':
    scene('day1', 'day', 7); scene('day2', 'day', 3); scene('cave1', 'cave', 5); scene('day3', 'day', 11)
