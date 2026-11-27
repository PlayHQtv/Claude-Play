#!/usr/bin/env python3
"""Content overlap check (user 26.11.2026: "Überschneiden sollte sich nichts").

A new post must not feature anything an earlier post already featured: the same weapon build (also inside a
ranking / loadout / meta-builds post), the same setting group, the same tip, the same news item.

Usage: python3 topic_check.py data/<file>.json
Every data file should carry "topic_keys": ["kg-7 vulcan", ...] = the things the post is ABOUT. If it is missing,
the keys are taken from the weapon titles and the cover title.
Exit 1 when a key appears in another post's content (not counting notes/sources/captions and the Apex catalogue
posts). A justified exception goes into "overlap_ok": {"<other file stem>": "reason"} and is reported, not hidden.
"""
import json, sys, glob, os, re

SKIP_FIELDS = {'notes', 'source', 'sources', 'caption', 'verified', 'wallpaper', 'img', 'hero', 'cutout', 'logo',
               'topic_keys', 'overlap_ok', 'style', 'badge', 'game'}
SKIP_FILES = re.compile(r'(example-|DISCARDED-|-apex|apex-official-source)', re.I)
# patch-note / update posts list many weapons as news; a weapon BUILD after a buff is not the same content.
# They only count against other news/update posts.
NEWS = re.compile(r'(update|patch-notes|patch|-season-\d|season-\d-|reloaded|-news)', re.I)


def text_of(x, out):
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in SKIP_FIELDS:
                text_of(v, out)
    elif isinstance(x, list):
        for v in x:
            text_of(v, out)
    elif isinstance(x, str):
        out.append(x)
    return out


def keys_of(d):
    keys = [k.lower() for k in d.get('topic_keys', [])]
    if not keys:
        for w in d.get('weapons', []):
            t = f"{w.get('title_white', '')} {w.get('title_gold', '')}".strip()
            if t:
                keys.append(t.lower())
        if not keys:
            print('topic: STOP - posts without a weapon build need "topic_keys" (what the post is about, e.g. ["aim assist", "response curve"])')
            sys.exit(1)
        print('topic: note - no "topic_keys", using the weapon titles', sorted(set(keys)))
    return keys


def norm(s):
    return re.sub(r'[^a-z0-9.]+', ' ', s.lower()).strip()


def main(path):
    d = json.load(open(path))
    keys = list(dict.fromkeys(norm(k) for k in keys_of(d)))
    news_me = bool(NEWS.search(os.path.basename(path)))
    ok = d.get('overlap_ok', {})
    me = os.path.basename(path)
    hits = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(path) or '.', '*.json'))):
        b = os.path.basename(f)
        if b == me or SKIP_FILES.search(b):
            continue
        if bool(NEWS.search(b)) != news_me:
            continue
        try:
            o = json.load(open(f))
        except Exception:
            continue
        t = ' ' + norm(' '.join(text_of(o, []))) + ' '
        for k in keys:
            if k and f' {k} ' in t and (k, b[:-5]) not in [(h[0], h[1]) for h in hits]:
                stem = b[:-5]
                if stem in ok:
                    print(f'topic: allowed overlap "{k}" with {stem} ({ok[stem]})')
                else:
                    hits.append((k, stem))
    for k, s in hits:
        print(f'topic: OVERLAP "{k}" already featured in {s}')
    if hits:
        print('topic: STOP - choose a topic nobody has seen on our account yet (or document a real reason in "overlap_ok")')
        sys.exit(1)
    print('topic: OK - no overlap with earlier posts')


if __name__ == '__main__':
    main(sys.argv[1])
