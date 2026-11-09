"""CPU vision helpers (ONNX Runtime, no GPU needed). Models are downloaded from GitHub releases into MODELS
(never committed):
  BiRefNet-general-lite.onnx (swin-tiny, local) / BiRefNet-general-epoch_244.onnx (full, runner: vision-hq workflow)
  vit_b-encoder-quant.onnx / -decoder  https://github.com/danielgatis/rembg/releases/download/v0.0.0/   (Segment Anything, point prompts)
  depth_anything_v2_vits.onnx          https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/v2.0.0/
bin/models.sh downloads them.  Local box (7 GB RAM): SAM + depth fine; BiRefNet -> vision-hq workflow.

  birefnet(img)              -> 'L' alpha mask (best general cut-outs: hair, weapons, vehicles)
  sam(img, points, labels)   -> 'L' mask of the object at the clicked point(s)
  depth(img)                 -> 'L' depth map (white = near)
"""
import os
import numpy as np
from PIL import Image

MODELS = os.environ.get('PHQ_MODELS', '/tmp/models')
_S = {}
MEAN = np.array([0.485, 0.456, 0.406], np.float32); STD = np.array([0.229, 0.224, 0.225], np.float32)


def _sess(name):
    if name not in _S:
        import onnxruntime as ort
        o = ort.SessionOptions(); o.intra_op_num_threads = os.cpu_count() or 2; o.enable_cpu_mem_arena = False
        _S[name] = ort.InferenceSession(os.path.join(MODELS, name), o, providers=['CPUExecutionProvider'])
    return _S[name]


def _norm(im, size):
    a = np.asarray(im.convert('RGB').resize(size, Image.BICUBIC), np.float32) / 255.
    return ((a - MEAN) / STD).transpose(2, 0, 1)[None]


def birefnet(img, full=False):
    # lite (swin-tiny) fits in 7 GB RAM; full (swin-large) needs ~16 GB -> run it on a GitHub runner
    s = _sess('BiRefNet-general-epoch_244.onnx' if full else 'BiRefNet-general-lite.onnx')
    y = s.run(None, {s.get_inputs()[0].name: _norm(img, (1024, 1024))})[0][0, 0]
    y = 1 / (1 + np.exp(-y))
    return Image.fromarray((y * 255).clip(0, 255).astype(np.uint8)).resize(img.size, Image.BICUBIC)


def depth(img):
    s = _sess('depth_anything_v2_vits.onnx')
    y = s.run(None, {s.get_inputs()[0].name: _norm(img, (518, 518))})[0][0]
    y = (y - y.min()) / (y.max() - y.min() + 1e-6)
    return Image.fromarray((y * 255).astype(np.uint8)).resize(img.size, Image.BICUBIC)


def sam(img, points, labels=None):
    """points: [(x, y), ...] in image pixels; labels 1 = object, 0 = background."""
    im = img.convert('RGB'); W, H = im.size; sc = 1024 / max(W, H)
    nw, nh = round(W * sc), round(H * sc)
    a = np.asarray(im.resize((nw, nh), Image.BICUBIC), np.float32)
    a = (a - np.array([123.675, 116.28, 103.53], np.float32)) / np.array([58.395, 57.12, 57.375], np.float32)
    x = np.zeros((1024, 1024, 3), np.float32); x[:nh, :nw] = a
    enc = _sess('vit_b-encoder-quant.onnx')
    emb = enc.run(None, {'x': x.transpose(2, 0, 1)[None]})[0]
    labels = labels or [1] * len(points)
    pc = np.array([[[px * sc, py * sc] for px, py in points] + [[0, 0]]], np.float32)
    pl = np.array([list(labels) + [-1]], np.float32)
    dec = _sess('vit_b-decoder-quant.onnx')
    _m, iou, low = dec.run(None, {'image_embeddings': emb, 'point_coords': pc, 'point_labels': pl,
                               'mask_input': np.zeros((1, 1, 256, 256), np.float32), 'has_mask_input': np.zeros(1, np.float32),
                               'orig_im_size': np.array([H, W], np.float32)})
    # the exported decoder's own upscaling ignores the padding (mask shifts vertically) -> use low_res_masks ourselves
    low = low[0, int(np.argmax(iou[0]))].astype(np.float32)
    L = np.asarray(Image.fromarray(low).resize((1024, 1024), Image.BILINEAR))[:nh, :nw]
    L = np.asarray(Image.fromarray(L).resize((W, H), Image.BILINEAR))
    return Image.fromarray((np.clip(L * 2.0 + 0.5, 0, 1) * 255).astype(np.uint8))


def largest(mask, thr=128):
    """Keep only the biggest connected blob (removes stray specks)."""
    from scipy import ndimage
    a = np.asarray(mask); lab, n = ndimage.label(a > thr)
    if n < 2: return mask
    k = 1 + int(np.argmax(ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))))
    return Image.fromarray(np.where(lab == k, a, 0).astype(np.uint8))


def cutout(img, mask, feather=1.2):
    """RGBA cut-out cropped to the object; light feather on the edge."""
    from PIL import ImageFilter
    m = mask.filter(ImageFilter.GaussianBlur(feather)) if feather else mask
    out = img.convert('RGBA'); out.putalpha(m)
    return out.crop(m.point(lambda v: 255 if v > 20 else 0).getbbox())
