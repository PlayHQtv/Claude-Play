"""Visual duplicate check (supports the duplicate rule): which images of a new carousel were already used in an
earlier post? Matches ORB keypoints (OpenCV, RANSAC homography) of every image a data JSON references against all other
data/*.json files, so a re-used screenshot is found even under another file name, re-graded, resized or cropped.
Blurred ambient backgrounds (*_amb, bg_*) are ignored.
Usage: python3 dupcheck.py data/<new>.json   -> prints matches, exit 1 if the COVER hero image was already used."""
import glob, json, os, re, sys
from PIL import Image
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DIRS = ['_build/gta', '_build/s1', '_build/w', 'weapons', 'assets', '_build']
_cache = {}


def find(name):
    for d in DIRS:
        p = os.path.join(HERE, d, name)
        if os.path.isfile(p): return p


def images(data_path):
    d = json.load(open(data_path)); s = json.dumps(d)
    names = [os.path.basename(n) for n in re.findall(r'"([^"]+\.(?:jpg|png))"', s)]
    cover = json.dumps(d.get('cover', {}) if isinstance(d, dict) else d[:1])
    return [(n, n in cover) for n in dict.fromkeys(names)]


def h(name):
    if name not in _cache:
        p = find(name); f = None
        if p and not (name.endswith('_amb.jpg') or name.startswith('bg_') or name in ('logo.png', 'grain.png', 'logo_gta6.png')):
            im = np.asarray(Image.open(p).convert('L')); sc = 800 / max(im.shape)
            f = cv2.ORB_create(1500).detectAndCompute(cv2.resize(im, None, fx=sc, fy=sc), None)
            if f[1] is None or len(f[0]) < 20: f = None
        _cache[name] = f
    return _cache[name]


def same(a, b):
    """Number of geometrically consistent keypoint matches (>= 40 = same source image)."""
    m = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(a[1], b[1], k=2)
    g = [x for x, y in (p for p in m if len(p) == 2) if x.distance < 0.75 * y.distance]
    if len(g) < 12: return len(g)
    H, mask = cv2.findHomography(np.float32([a[0][x.queryIdx].pt for x in g]), np.float32([b[0][x.trainIdx].pt for x in g]), cv2.RANSAC, 5.0)
    return int(mask.sum()) if mask is not None else 0


def main(new):
    new = os.path.abspath(new); hard = False
    mine = [(n, c, h(n)) for n, c in images(new)]
    for other in sorted(glob.glob(os.path.join(HERE, 'data', '*.json'))):
        if os.path.abspath(other) == new or 'example' in os.path.basename(other): continue
        for on, _ in images(other):
            oh = h(on)
            if oh is None: continue
            for n, cover, nh in mine:
                if nh is not None and (k := same(nh, oh)) >= 40:
                    print(f'{"COVER " if cover else ""}image {n} = {on} in {os.path.basename(other)} ({k} matching points)'); hard |= cover
    print('dupcheck:', 'cover image already used -> pick another hero image' if hard else 'OK')
    return not hard


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1]) else 1)
