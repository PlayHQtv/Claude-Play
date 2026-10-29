"""QA helper: draws the TikTok photo-mode UI (measured from a real screenshot, 29.10.2026) over 1080x1440 slides.
Usage: python3 tiktok_overlay.py out/<name>  -> out/<name>/_qa/*.jpg + _qa/sheet.jpg"""
import sys, os, glob
from PIL import Image, ImageDraw
d = sys.argv[1]; q = os.path.join(d, '_qa'); os.makedirs(q, exist_ok=True)
ZONES = [  # (x0,y0,x1,y1) in 1080x1440 image coordinates
    (20, 22, 1040, 114),     # search bar / top tabs
    (942, 180, 1048, 240),   # "2 / 6" counter
    (940, 1100, 1080, 1440), # avatar, like, comment, save buttons (right column)
    (30, 1320, 800, 1440),   # first-comment bubble / caption
]
ims = []
for f in sorted(glob.glob(os.path.join(d, '*.jpg'))):
    im = Image.open(f).convert('RGB'); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    for z in ZONES: dr.rectangle(z, fill=(255, 0, 60, 90), outline=(255, 0, 60, 255), width=3)
    out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); out.save(os.path.join(q, os.path.basename(f))); ims.append(out)
w = 360; sheet = Image.new('RGB', (w * len(ims), 480))
for i, im in enumerate(ims): sheet.paste(im.resize((w, 480)), (i * w, 0))
sheet.save(os.path.join(q, 'sheet.jpg')); print(os.path.join(q, 'sheet.jpg'))
