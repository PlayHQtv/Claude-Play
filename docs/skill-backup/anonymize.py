"""Anonymize the skill before it goes into this PUBLIC repo.
Usage: python3 anonymize.py <SKILL.md> <out.md>
Replaces account IDs, cloud names, trigger IDs, post UUIDs, OpusClip project/clip IDs, our own handle and e-mails with placeholders."""
import re, sys

RULES = [
    (r'[\w.+-]+@[\w-]+\.[\w.]+', '<EMAIL>'),
    (r'\btrig_[A-Za-z0-9]+', '<TRIGGER_ID>'),
    (r'\bBLOG_ID\b', '<METRICOOL_BLOG_ID>'),
    (r'\bCLOUD_NAME\b', '<CLOUDINARY_CLOUD>'),
    (r'\b6ac1[0-9a-f]{20}\b', '<OPUSCLIP_ACCOUNT_ID>'),
    (r'\bP31[0-9]{5}[A-Za-z0-9]{4}\b', '<OPUSCLIP_PROJECT_ID>'),
    (r'(?<![\w/-])-?\d{15,20}(?![\w])', '<POST_UUID>'),
    (r'\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])[A-Za-z0-9]{10,12}\b', '<CLIP_ID>'),
    (r'@playhqtv', '<OUR_TIKTOK_HANDLE>'),
    # clip IDs without digits: 10-12 letters, mixed case, not a normal CamelCase word (whitelist below)
    (r'\b(?!(?:MrMarvelTV|SiNisterFPS|autoAddMusic|MrRoflWaffles)\b)(?=[A-Za-z]{10,12}\b)(?=(?:[a-z]*[A-Z]){2})(?=[A-Z]*[a-z])(?![A-Z][a-z]+(?:[A-Z][a-z]+)*\b)[A-Za-z]{10,12}\b', '<CLIP_ID>'),
    (r'\bAPI_KEY\b', '<CLOUDINARY_API_KEY>'),
]


def anon(text):
    for pat, rep in RULES:
        text = re.sub(pat, rep, text, flags=re.I if pat == '@playhqtv' else 0)
    return text


if __name__ == '__main__':
    src, out = sys.argv[1:3]
    t = anon(open(src).read())
    open(out, 'w').write(t)
    for pat, rep in RULES:
        print(rep, t.count(rep))
