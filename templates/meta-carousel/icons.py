"""Generates the gold HUD line icons (assets/icons/<type>.svg).
Style: 2.4px gold outline + faint gradient fill + soft glow, viewBox 160x90.
Add a new attachment type by adding a key to ICONS. Run: python3 icons.py"""
import os

S = 'stroke="#ffd76a" stroke-width="2.4" fill="url(#f)" stroke-linejoin="round" stroke-linecap="round"'
T = 'stroke="#ffd76a" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".85"'
DOT = 'fill="#ffd76a"'
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 90"><defs>'
        '<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd76a" stop-opacity=".38"/>'
        '<stop offset="1" stop-color="#ffd76a" stop-opacity=".06"/></linearGradient>'
        '<filter id="g" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g filter="url(#g)">')

ICONS = {
 'barrel': f'<path {S} d="M8 41 h104 v8 h-104 z"/><path {S} d="M112 37 h22 a3 3 0 0 1 3 3 v10 a3 3 0 0 1 -3 3 h-22 z"/>'
           f'<path {S} d="M58 35 h14 v20 h-14 z"/><path {S} d="M137 40 h14 v10 h-14 z"/>'
           f'<path {T} d="M14 45 h40 M76 45 h32 M118 41 v8 M124 41 v8 M130 41 v8 M62 39 v12 M68 39 v12"/>',
 'muzzle': f'<path {S} d="M14 32 h96 a6 6 0 0 1 6 6 v14 a6 6 0 0 1 -6 6 h-96 a4 4 0 0 1 -4 -4 v-18 a4 4 0 0 1 4 -4 z"/>'
           f'<path {S} d="M116 38 h22 v14 h-22 z"/><path {S} d="M138 35 h10 v20 h-10 z"/>'
           f'<path {T} d="M24 40 h28 a5 5 0 0 1 0 10 h-28 a5 5 0 0 1 0 -10 z M62 40 h28 a5 5 0 0 1 0 10 h-28 a5 5 0 0 1 0 -10 z M100 34 v22 M106 34 v22"/>',
 'optic': f'<path {S} d="M22 62 h116 v10 h-116 z"/><path {S} d="M34 62 v-14 a6 6 0 0 1 6 -6 h52 v20 z"/>'
          f'<path {S} d="M92 62 v-38 a6 6 0 0 1 6 -6 h22 a6 6 0 0 1 6 6 v38 z"/><path {T} d="M100 26 h18 v28 h-18 z"/>'
          f'<circle cx="109" cy="40" r="3.2" {DOT}/><path {T} d="M42 50 h40 M30 67 h4 M44 67 h4 M58 67 h4 M72 67 h4 M86 67 h4 M100 67 h4 M114 67 h4 M128 67 h4"/>'
          f'<circle cx="64" cy="50" r="4" {T}/>',
 'underbarrel': f'<path {S} d="M24 16 h112 v12 h-112 z"/><path {S} d="M58 28 h44 l-12 42 a8 8 0 0 1 -8 6 h-8 a6 6 0 0 1 -6 -7 z"/>'
                f'<path {T} d="M30 22 h4 M42 22 h4 M54 22 h4 M66 22 h4 M78 22 h4 M90 22 h4 M102 22 h4 M114 22 h4 M126 22 h4 M70 40 h22 M68 48 h20 M66 56 h18"/>',
 'reargrip': f'<path {S} d="M54 14 h50 l2 10 l-10 4 l16 50 a6 6 0 0 1 -5 8 h-22 a6 6 0 0 1 -6 -5 l-14 -50 z"/>'
             f'<path {T} d="M74 34 l12 40 M84 32 l12 40 M66 36 l10 36 M58 20 h40"/>',
 'stock': f'<path {S} d="M10 30 h40 v14 h-40 z"/><path {S} d="M50 26 h18 v22 h-18 z"/>'
          f'<path {S} d="M68 30 l60 -8 a6 6 0 0 1 7 6 l4 40 a6 6 0 0 1 -6 6 h-10 l-14 -20 h-41 z"/>'
          f'<path {T} d="M16 37 h28 M80 40 l40 -6 M122 34 l3 30 M56 30 v14"/>',
 'magazine': f'<path {S} d="M58 8 h40 l-2 10 h-36 z"/><path {S} d="M60 18 h36 l-4 58 a6 6 0 0 1 -6 6 h-16 a6 6 0 0 1 -6 -6 z"/>'
             f'<path {T} d="M68 28 l-1 44 M78 28 v48 M88 28 l-1 44 M62 82 h32"/>',
 'drum': f'<path {S} d="M64 8 h28 v14 h-28 z"/><circle cx="78" cy="52" r="30" {S}/><circle cx="78" cy="52" r="18" {T}/>'
         f'<circle cx="78" cy="52" r="5" {DOT}/><path {T} d="M78 22 v6 M78 76 v6 M48 52 h6 M102 52 h6"/>',
 'ammo': ''.join(f'<path {S} d="M{x} 78 v-38 l8 -24 l8 24 v38 z"/><path {T} d="M{x} 46 h16 M{x} 70 h16"/>'
                 for x in (46, 72, 98)),
 'apex': f'<path {S} d="M80 8 l34 20 v34 l-34 20 l-34 -20 v-34 z"/><path {T} d="M80 22 l22 13 v20 l-22 13 l-22 -13 v-20 z"/>'
         f'<circle cx="80" cy="45" r="6" {DOT}/><path {T} d="M20 45 h22 M118 45 h22"/>',
 'laser': f'<path {S} d="M30 26 h66 a6 6 0 0 1 6 6 v24 a6 6 0 0 1 -6 6 h-66 z"/><path {S} d="M102 34 h12 v20 h-12 z"/>'
          f'<path {T} d="M40 36 h30 M40 44 h20 M40 52 h26"/><circle cx="84" cy="44" r="5" {T}/>'
          f'<path stroke="#ffd76a" stroke-width="2" d="M114 44 h36" opacity=".9"/>',
 'comb': f'<path {S} d="M18 40 h124 l-8 22 h-108 z"/><path {T} d="M30 50 h96 M18 40 l10 -12 h104 l10 12"/>',
}

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icons')
    os.makedirs(out, exist_ok=True)
    for k, v in ICONS.items():
        open(os.path.join(out, f'{k}.svg'), 'w').write(HEAD + v + '</g></svg>')
    print('icons:', ', '.join(ICONS))
