"""Encrypt a value (URL, params) for the PUBLIC repo with fx/pubkey.pem. The GitHub runners decrypt it with the
private key that lives only in the draft release "grab-private". Output: enc:<b64 rsa-oaep key>:<b64 aes-256-cbc data>
Usage: python3 tools/secure.py "<text>"   (prints one line)"""
import base64, os, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def enc(text):
    with tempfile.TemporaryDirectory() as d:
        open(f'{d}/k', 'wb').write(os.urandom(32).hex().encode())
        open(f'{d}/t', 'w').write(text)
        subprocess.run(['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', f'{REPO}/fx/pubkey.pem', '-pkeyopt', 'rsa_padding_mode:oaep', '-in', f'{d}/k', '-out', f'{d}/k.enc'], check=True)
        subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt', '-pass', f'file:{d}/k', '-in', f'{d}/t', '-out', f'{d}/t.enc'], check=True)
        return 'enc:' + base64.b64encode(open(f'{d}/k.enc', 'rb').read()).decode() + ':' + base64.b64encode(open(f'{d}/t.enc', 'rb').read()).decode()


if __name__ == '__main__':
    print(enc(sys.argv[1]))
