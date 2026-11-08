"""PlayHQ colour grade for photos/screenshots (not for UI or weapon renders).
Look: deep neutral-warm blacks, gentle S-curve, warm gold highlights, slightly calmer blues, +vibrance.
Usage: python3 grade.py <in> <out> [strength 0..1]   or  import grade; grade.apply(PIL_image)"""
import sys
import numpy as np
from PIL import Image


def _curve(x, strength):
    # filmic S-curve: deeper blacks, punchier mids, soft highlight roll-off
    k = 1 + 0.9 * strength
    y = 1 / (1 + np.exp(-k * 4 * (x - 0.5)))
    y0, y1 = 1 / (1 + np.exp(k * 2)), 1 / (1 + np.exp(-k * 2))
    y = (y - y0) / (y1 - y0)
    return x + (y - x) * 0.55 * strength


def apply(im, strength=1.0):
    a = np.asarray(im.convert('RGB'), dtype=np.float32) / 255.
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    # warm white balance, stronger in highlights (gold), neutral in shadows
    w = np.clip(lum, 0, 1)[..., None] * strength
    a = a * (1 + w * np.array([0.06, 0.02, -0.07], dtype=np.float32))
    # +12% saturation around luminance
    l2 = (a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    a = l2 + (a - l2) * (1 + 0.12 * strength)
    a = _curve(np.clip(a, 0, 1), strength)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


if __name__ == '__main__':
    apply(Image.open(sys.argv[1]), float(sys.argv[3]) if len(sys.argv) > 3 else 1.0).save(sys.argv[2], quality=95)
