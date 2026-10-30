"""Writes fx/jobs/<name>.json for the fx-render workflow.
The signed Cloudinary upload params (they contain account metadata) are encrypted with the repo's fx/pubkey.pem
(RSA-OAEP for a random key + AES-256-CBC/pbkdf2 via openssl), so nothing readable lands in the public repo.
Usage: python3 make_job.py <name> <src_url> <signed_upload.json (outside the repo)> [fx.json]"""
import base64, json, os, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main(name, src_url, signed, fxp=None):
    up = json.load(open(signed))
    if isinstance(up, list):
        up = up[0]
    with tempfile.TemporaryDirectory() as d:
        key = os.urandom(32).hex().encode()
        open(f'{d}/k', 'wb').write(key)
        open(f'{d}/up.json', 'w').write(json.dumps(up))
        subprocess.run(['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', f'{REPO}/fx/pubkey.pem', '-pkeyopt', 'rsa_padding_mode:oaep',
                        '-in', f'{d}/k', '-out', f'{d}/k.enc'], check=True)
        subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt', '-pass', f'file:{d}/k', '-in', f'{d}/up.json', '-out', f'{d}/up.enc'], check=True)
        job = {'src_url': src_url, 'fx': json.load(open(fxp)) if fxp else {},
               'key_enc': base64.b64encode(open(f'{d}/k.enc', 'rb').read()).decode(),
               'upload_enc': base64.b64encode(open(f'{d}/up.enc', 'rb').read()).decode()}
    os.makedirs(f'{REPO}/fx/jobs', exist_ok=True)
    out = f'{REPO}/fx/jobs/{name}.json'
    json.dump(job, open(out, 'w'), indent=1)
    print(out)


if __name__ == '__main__':
    main(*sys.argv[1:])
