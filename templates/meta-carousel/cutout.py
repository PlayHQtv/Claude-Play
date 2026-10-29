"""Cut a weapon out of its background (free ISNet model from the rembg project, runs offline with onnxruntime).
Usage: python3 cutout.py <input.png> <weapons/name.png>
The model (~180 MB) is downloaded once from GitHub into ./models (gitignored)."""
import os, sys, urllib.request
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, 'models', 'isnet-general-use.onnx')
URL = 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx'


def session():
    import onnxruntime as ort
    if not os.path.exists(MODEL):
        os.makedirs(os.path.dirname(MODEL), exist_ok=True)
        print('downloading model ...'); urllib.request.urlretrieve(URL, MODEL)
    return ort.InferenceSession(MODEL)


def cut(src, dst, sess=None):
    sess = sess or session()
    im = Image.open(src).convert('RGB')
    x = np.asarray(im.resize((1024, 1024), Image.LANCZOS), dtype=np.float32) / 255. - 0.5
    m = sess.run(None, {sess.get_inputs()[0].name: x.transpose(2, 0, 1)[None]})[0][0, 0]
    m = (m - m.min()) / (m.max() - m.min() + 1e-8)
    mask = Image.fromarray((m * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)
    im.putalpha(mask)
    box = Image.fromarray(((np.asarray(mask) > 40) * 255).astype(np.uint8)).getbbox()
    im.crop(box).save(dst)
    print(dst, im.crop(box).size)


if __name__ == '__main__':
    cut(sys.argv[1], sys.argv[2])
