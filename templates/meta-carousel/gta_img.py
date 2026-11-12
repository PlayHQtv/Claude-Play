"""Prepare an official GTA 6 screenshot for gta3_render: graded shot g_<name>.jpg + blurred ambient g_<name>_amb.jpg.
Usage: python3 gta_img.py <raw.jpg> <name>   -> _build/gta/g_<name>.jpg, _build/gta/g_<name>_amb.jpg (private, never committed)."""
import os, sys
from PIL import Image, ImageEnhance, ImageFilter
import grade

HERE = os.path.dirname(os.path.abspath(__file__))


def main(src, name):
    out = os.path.join(HERE, '_build', 'gta')
    im = Image.open(src).convert('RGB')
    g = grade.apply(im)
    g.save(os.path.join(out, f'g_{name}.jpg'), quality=95)
    W, H = 2160, 2880  # 3:4 cover crop for the ambient background
    s = max(W / g.width, H / g.height)
    a = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
    l, t = (a.width - W) // 2, (a.height - H) // 2
    a = a.crop((l, t, l + W, t + H)).resize((540, 720), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28)).resize((W, H), Image.LANCZOS)
    ImageEnhance.Brightness(a).enhance(0.5).save(os.path.join(out, f'g_{name}_amb.jpg'), quality=90)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
