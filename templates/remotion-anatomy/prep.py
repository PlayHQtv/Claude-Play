"""Builds public/ for a Remotion anatomy job: rifle.png, edge.png (gold wireframe), xray.png, grain0-3.png, fonts, logo, sfx, bed.
usage: python3 prep.py <job.json>   (run from templates/remotion-anatomy, repo root = ../..)"""
import json, sys, os, shutil, numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageChops
job = json.load(open(sys.argv[1])); R = '../..'; P = 'public'
shutil.rmtree(P, ignore_errors=True); os.makedirs(P + '/fonts'); os.makedirs(P + '/sfx')
im = Image.open(os.path.join(R, job['weapon'])).convert('RGBA'); im.save(P + '/rifle.png')
a = im.split()[3]; lum = ImageOps.grayscale(im)
e1 = lum.filter(ImageFilter.FIND_EDGES).point(lambda v: min(255, v * 4))
outer = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(5)), a.filter(ImageFilter.MinFilter(3)))
edge = ImageChops.lighter(ImageChops.multiply(e1, a), outer).filter(ImageFilter.GaussianBlur(0.6)).point(lambda v: min(255, int(v * 1.6)))
g = Image.new('RGBA', im.size, (255, 212, 0, 0)); g.putalpha(edge); g.save(P + '/edge.png')
L = np.array(lum).astype(float) / 255; inv = 1 - L; al = np.array(a).astype(float) / 255
x = np.stack([inv * 120 + 40, inv * 220 + 30, inv * 255, al * (0.35 + 0.65 * inv) * 255], -1).clip(0, 255).astype('uint8')
Image.fromarray(x, 'RGBA').save(P + '/xray.png')
rng = np.random.default_rng(1)
for i in range(4): Image.fromarray((rng.random((960, 540)) * 255).astype('uint8'), 'L').resize((1080, 1920), Image.NEAREST).save(f'{P}/grain{i}.png')
F = R + '/templates/meta-carousel/assets'
for f in ['Anton-Regular.ttf', 'Rajdhani-Bold.ttf', 'Rajdhani-SemiBold.ttf']: shutil.copy(f'{F}/fonts/{f}', f'{P}/fonts/{f}')
shutil.copy(R + '/brand/playhq-logo.png' if os.path.exists(R + '/brand/playhq-logo.png') else F + '/logo.png', P + '/logo.png')
for s in job.get('sfx', []):
    d = f"{P}/sfx/{os.path.dirname(s['file'])}"; os.makedirs(d, exist_ok=True); shutil.copy(f"{R}/assets/sfx/kenney/{s['file']}", f"{P}/sfx/{s['file']}")
if job.get('bed'): shutil.copy('assets/' + job['bed'], P + '/' + job['bed'])
props = {k: v for k, v in job.items() if k not in ('weapon', 'name')}; props['img'] = {'w': im.size[0], 'h': im.size[1]}
json.dump(props, open('/tmp/props.json', 'w')); print('prep ok', im.size, len(job.get('sfx', [])), 'sfx')
