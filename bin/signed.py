"""signed.py <upload_dir> <timestamp> <audit_context> <id=sig> [id=sig ...]  -> <upload_dir>/signed.json (stays outside the repo).
Cloud name, api key and preset come from env PHQ_CLOUD / PHQ_KEY / PHQ_PRESET (never stored in the repo)."""
import json, os, sys
d, ts, ac, pairs = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4:]
out = [{"upload_params": {"colors": 0, "overwrite": True, "public_id": "playhq/tmp/" + p.split('=')[0], "timestamp": ts,
        "upload_preset": os.environ['PHQ_PRESET'], "audit_context": ac}, "api_key": os.environ['PHQ_KEY'], "signature": p.split('=')[1],
        "host": "api.cloudinary.com", "cloud_name": os.environ['PHQ_CLOUD']} for p in pairs]
json.dump(out, open(os.path.join(d, 'signed.json'), 'w')); print(len(out), 'signed')
