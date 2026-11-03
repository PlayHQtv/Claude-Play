"""Synthesized (copyright-free) sound bed for the FREEZE + MARKUP pause (user wish 04.11.2026: no silent gap).
make(durations, path): freeze hit (whoosh down + thump) -> soft drone + clock tick -> pop per markup step ->
two-tone hit for the verdict banner -> rising whoosh back into the clip. 48 kHz stereo WAV."""
import numpy as np, wave

SR = 48000


def _env(n, a=0.005, r=None):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if r: e *= np.exp(-np.arange(n) / (r * SR))
    return e


def _noise_sweep(d, f0, f1):
    n = int(d * SR); x = np.random.default_rng(1).standard_normal(n)
    out = np.zeros(n); f = np.linspace(f0, f1, n); y1 = y2 = 0.0
    for i in range(n):  # simple resonant band-pass that sweeps
        w = 2 * np.pi * f[i] / SR; q = 0.08
        y = x[i] * q + 2 * (1 - q) * np.cos(w) * y1 - (1 - q) ** 2 * y2
        out[i], y2, y1 = y, y1, y
    out /= np.abs(out).max() + 1e-9
    return out * np.sin(np.linspace(0, np.pi, n)) ** 1.5


def _tone(d, f0, f1=None, decay=0.08):
    n = int(d * SR); f = np.linspace(f0, f1 or f0, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, decay)


def make(durations, path, level=0.5):
    total = sum(durations); n = int(total * SR); s = np.zeros(n)

    def put(x, at, g):
        i = int(at * SR); j = min(n, i + len(x)); s[i:j] += x[:j - i] * g
    put(_noise_sweep(0.35, 5000, 300), 0, 0.55)                  # freeze whoosh
    put(_tone(0.4, 90, 40, 0.12), 0, 0.9)                        # thump
    t = np.arange(n) / SR                                         # drone bed
    bed = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 110 * t)) * (0.75 + 0.25 * np.sin(2 * np.pi * 3 * t))
    fade = np.minimum(1, np.minimum(t / 0.25, (total - t) / 0.3)).clip(0)
    s += bed * fade * 0.12
    for k in np.arange(0.3, total - 0.3, 0.5):                    # clock tick
        put(_tone(0.03, 2400, 2400, 0.006), k, 0.18)
    cum = np.cumsum([0] + list(durations))
    for k in cum[1:-2]:                                           # pop per markup step
        put(_tone(0.12, 1300, 700, 0.04), k, 0.6)
        put(_noise_sweep(0.05, 3000, 3000), k, 0.15)
    hit = cum[-2]                                                 # banner hit
    put(_tone(0.6, 880, 880, 0.15) + 0.7 * _tone(0.6, 1320, 1320, 0.12), hit, 0.45)
    put(_tone(0.3, 70, 45, 0.1), hit, 0.7)
    put(_noise_sweep(0.35, 300, 5000), total - 0.35, 0.45)        # rise back into the clip
    s = s / (np.abs(s).max() + 1e-9) * level
    st = (np.stack([s, s], 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
