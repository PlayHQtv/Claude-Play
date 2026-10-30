"""Anonymize the skill before it goes into this PUBLIC repo. Only generic patterns, no real values in this file.
Usage: python3 anonymize.py <SKILL.md> <out.md>"""
import re, sys

RULES = [
    (r'[\w.+-]+@[\w-]+\.[a-z]{2,}', '<EMAIL>'),
    (r'\btrig_[A-Za-z0-9]+', '<TRIGGER_ID>'),
    (r'(res\.cloudinary\.com/)[a-z0-9_-]+', r'\1<CLOUDINARY_CLOUD>'),
    (r'(cloud `)[a-z0-9_-]+(`)', r'\1<CLOUDINARY_CLOUD>\2'),
    (r'(blogId[^`]*`)\d+(`)', r'\1<METRICOOL_BLOG_ID>\2'),
    (r'\b\d{6,8}\b(?![./:-]\d)', '<ID>'),
    (r'\b[0-9a-f]{24}\b', '<ACCOUNT_ID>'),
    (r'\bP\d{7}[A-Za-z0-9]{4}\b', '<OPUSCLIP_PROJECT_ID>'),
    (r'(?<![\w/-])-?\d{13,20}(?![\w])', '<LONG_ID>'),
    (r'\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])[A-Za-z0-9]{10,12}\b', '<CLIP_ID>'),
    (r'\b(?!(?:MrMarvelTV|SiNisterFPS|autoAddMusic|MrRoflWaffles)\b)(?=[A-Za-z]{10,12}\b)(?=(?:[a-z]*[A-Z]){2})(?=[A-Z]*[a-z])(?![A-Z][a-z]+(?:[A-Z][a-z]+)*\b)[A-Za-z]{10,12}\b', '<CLIP_ID>'),
    (r'(?i)@playhqtv\b', '<OUR_TIKTOK_HANDLE>'),
]


def anon(text):
    for pat, rep in RULES:
        text = re.sub(pat, rep, text)
    return text


if __name__ == '__main__':
    src, out = sys.argv[1:3]
    open(out, 'w').write(anon(open(src).read()))
