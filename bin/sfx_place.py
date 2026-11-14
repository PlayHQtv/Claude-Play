#!/usr/bin/env python3
"""Put real sound effects onto the exact frame of a video (own take on the "RealSFX" idea).

Usage:
  python3 bin/sfx_place.py in.mp4 out.mp4 F12:whoosh F60:impact:-6 2.5s:pop
  python3 bin/sfx_place.py in.mp4 out.mp4 --cues cues.txt          # one cue per line, same syntax

Cue = <when>:<sound>[:<gain dB>]
  when  = F<frame> (exact frame, fps read from the video) or <seconds>s
  sound = name in assets/sfx/openverse/ or assets/sfx/kenney/**/ (without .ogg), or a path to an audio file
The original audio stays and the effects are mixed on top, the video stream is copied untouched. Requires ffmpeg/ffprobe.
"""
import glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fps_of(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                        '-of', 'json', path], capture_output=True, text=True, check=True)
    n, d = json.loads(r.stdout)['streams'][0]['r_frame_rate'].split('/')
    return float(n) / float(d)


def has_audio(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def find_sound(name):
    if os.path.isfile(name): return name
    for pat in (f'assets/sfx/openverse/{name}.ogg', f'assets/sfx/kenney/**/{name}.ogg', f'assets/sfx/**/{name}.*'):
        hits = sorted(glob.glob(os.path.join(ROOT, pat), recursive=True))
        if hits: return hits[0]
    sys.exit(f'sound not found: {name} (see assets/sfx/openverse/CREDITS.txt and assets/sfx/kenney/INDEX.txt)')


def parse(cue, fps):
    parts = cue.split(':'); when, snd = parts[0], parts[1]; gain = float(parts[2]) if len(parts) > 2 else 0.0
    t = int(when[1:]) / fps if when.upper().startswith('F') else float(when.rstrip('s'))
    return t, find_sound(snd), gain


def main(a):
    if len(a) < 3: sys.exit(__doc__)
    src, dst, rest = a[0], a[1], a[2:]
    if rest[0] == '--cues': rest = [l.strip() for l in open(rest[1]) if l.strip() and not l.startswith('#')]
    fps = fps_of(src); cues = [parse(c, fps) for c in rest]
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', src]
    for _, s, _ in cues: cmd += ['-i', s]
    f, labels = [], []
    for i, (t, _, g) in enumerate(cues, 1):
        ms = int(round(t * 1000))
        f.append(f'[{i}:a]aresample=48000,volume={g}dB,adelay={ms}|{ms}[s{i}]'); labels.append(f'[s{i}]')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                               capture_output=True, text=True).stdout.strip() or 0)
    base = '[0:a]aresample=48000[b];' if has_audio(src) else f'anullsrc=r=48000:cl=stereo,atrim=duration={dur}[b];'
    f = base + ';'.join(f) + f';[b]{"".join(labels)}amix=inputs={len(cues) + 1}:duration=first:normalize=0,alimiter=limit=0.89[out]'
    cmd += ['-filter_complex', f, '-map', '0:v', '-map', '[out]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', dst]
    subprocess.run(cmd, check=True)
    for t, s, g in cues: print(f'{t:7.3f}s  F{round(t * fps):>5}  {os.path.basename(s)}  {g:+.0f} dB')
    print('->', dst)


if __name__ == '__main__':
    main(sys.argv[1:])
