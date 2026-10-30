"""PlayHQ TIP carousel in the "Part 1" look (5 MW4 DMZ mistakes, 28.10.2026 – our best carousel).
Usage: python3 tip_render.py data/<file>.json <frames_dir> <out_dir>
Look: blurred + darkened gameplay background, red label, yellow headline + white subline (Arial-style bold),
gameplay still in a yellow frame, two-line fix in black boxes (white + yellow). 1080x1440 (3:4, TikTok photo view).
Frames are third-party footage -> frames_dir and out_dir stay OUTSIDE the public repo."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

W, H = 1080, 1440
FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'  # metric-compatible with Arial Bold
Y, WH, RED = (255, 212, 0), (255, 255, 255), (225, 6, 0)


def f(size):
    return ImageFont.truetype(FONT, size)


def fit(d, text, size, max_w):
    while d.textlength(text, font=f(size)) > max_w and size > 20:
        size -= 2
    return f(size)


def bg(frame):
    b = frame.copy()
    s = max(W / b.width, H / b.height)
    b = b.resize((int(b.width * s) + 1, int(b.height * s) + 1), Image.LANCZOS)
    l, t = (b.width - W) // 2, (b.height - H) // 2
    b = b.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(28))
    return ImageEnhance.Brightness(b).enhance(0.42)


def shadow_text(d, xy, text, font, fill, anchor='mt', sw=3):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=(0, 0, 0))


def label(d, y, text):
    fo = f(34)
    w = d.textlength(text, font=fo)
    d.rectangle(((W - w) / 2 - 14, y, (W + w) / 2 + 14, y + 48), fill=RED)
    d.text((W / 2, y + 24), text, font=fo, fill=WH, anchor='mm')


def box_line(d, y, text, color, size=44):
    fo = fit(d, text, size, 900)
    w = d.textlength(text, font=fo)
    d.rectangle(((W - w) / 2 - 14, y, (W + w) / 2 + 14, y + size + 18), fill=(0, 0, 0))
    d.text((W / 2, y + (size + 18) / 2), text, font=fo, fill=color, anchor='mm')


def framed(im, frame, top, width=1000):
    fr = frame.resize((width, int(frame.height * width / frame.width)), Image.LANCZOS)
    fr = fr.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    x = (W - width) // 2
    d = ImageDraw.Draw(im)
    d.rectangle((x - 6, top - 6, x + width + 5, top + fr.height + 5), fill=Y)
    im.paste(fr, (x, top))
    return top + fr.height


def slide(frame, d0, kind, it=None):
    im = bg(frame)
    d = ImageDraw.Draw(im)
    label(d, 170, d0['label'])
    if kind == 'cover':
        c = d0['cover']
        shadow_text(d, (W / 2, 250), c['line1'], fit(d, c['line1'], 104, 960), Y)
        shadow_text(d, (W / 2, 362), c['line2'], fit(d, c['line2'], 104, 960), WH)
        box_line(d, 486, c['sub'], WH, 40)
        bottom = framed(im, frame, 580)
        d = ImageDraw.Draw(im)
        fo = f(40); w = d.textlength(c['swipe'], font=fo)
        d.rectangle(((W - w) / 2 - 14, bottom + 40, (W + w) / 2 + 14, bottom + 98), fill=Y)
        d.text((W / 2, bottom + 69), c['swipe'], font=fo, fill=(0, 0, 0), anchor='mm')
    elif kind == 'tip':
        shadow_text(d, (W / 2, 252), f'MISTAKE #{it["n"]}', f(100), Y)
        shadow_text(d, (W / 2, 372), it['title'], fit(d, it['title'], 64, 980), WH)
        bottom = framed(im, frame, 480)
        d = ImageDraw.Draw(im)
        box_line(d, bottom + 40, it['fix1'], WH)
        box_line(d, bottom + 112, it['fix2'], Y)
    return im


def cta(frame, d0):
    c = d0['cta']
    im = bg(frame)
    im = ImageEnhance.Brightness(im).enhance(0.7)
    d = ImageDraw.Draw(im)
    label(d, 170, d0['label'])
    shadow_text(d, (W / 2, 420), c['line1'], fit(d, c['line1'], 104, 960), Y)
    shadow_text(d, (W / 2, 535), c['line2'], fit(d, c['line2'], 104, 960), WH)
    fo = f(48); w = d.textlength(c['comment'], font=fo)
    d.rectangle(((W - w) / 2 - 18, 720, (W + w) / 2 + 18, 790), fill=Y)
    d.text((W / 2, 755), c['comment'], font=fo, fill=(0, 0, 0), anchor='mm')
    box_line(d, 840, c['follow'], WH, 44)
    box_line(d, 920, c['part1'], Y, 40)
    shadow_text(d, (W / 2, 1040), c['credit'], f(30), WH, sw=2)
    return im


def main(data_path, frames_dir, out_dir):
    d0 = json.load(open(data_path))
    os.makedirs(out_dir, exist_ok=True)
    fr = lambda n: Image.open(os.path.join(frames_dir, n)).convert('RGB')
    pages = [('01_cover', slide(fr(d0['cover']['frame']), d0, 'cover'))]
    for it in d0['tips']:
        pages.append((f'{len(pages) + 1:02d}_mistake_{it["n"]:02d}', slide(fr(it['frame']), d0, 'tip', it)))
    pages.append((f'{len(pages) + 1:02d}_cta', cta(fr(d0['cta']['frame']), d0)))
    for n, im in pages:
        p = os.path.join(out_dir, n + '.jpg')
        im.save(p, 'JPEG', quality=95, subsampling=0, optimize=True)
        print(p)


if __name__ == '__main__':
    main(*sys.argv[1:])
