#!/bin/bash
# bundle.sh <dir with signed.json + files named basename(public_id).jpg> -> encrypted upload via a NEW temporary branch,
# the workflow uploads to Cloudinary, prints the log (public_id, version, bytes) and deletes the branch itself.
set -e
W=$1; cd "$(dirname "$0")/.."; RM=$(git remote | head -1)
openssl rand -hex 32 | tr -d '\n' > $W/k
(cd $W && tar -cf - signed.json $(ls $W | grep -vE '^(signed.json|k|data.enc|key.enc)$')) | openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:$W/k -out $W/data.enc
openssl pkeyutl -encrypt -pubin -inkey fx/pubkey.pem -pkeyopt rsa_padding_mode:oaep -in $W/k -out $W/key.enc
B=tmp-upload-$(date +%s); CUR=$(git branch --show-current)
git checkout -q -b $B && mkdir -p bundle && cp $W/key.enc $W/data.enc bundle/ && git add -f bundle/key.enc bundle/data.enc
git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -m "bundle" && git push -q $RM $B 2>&1 | grep -iE "error|reject" || true
H=$(git rev-parse HEAD); git checkout -q $CUR && git branch -D -q $B; rm -f $W/k $W/signed.json $W/data.enc $W/key.enc
for i in $(seq 1 60); do
  s=$(gh run list -R PlayHQtv/Claude-Play -w upload-bundle -L 5 --json status,databaseId,headSha -q ".[]|select(.headSha==\"$H\")|\"\(.status) \(.databaseId)\"" 2>/dev/null || true)
  case "$s" in completed*) break;; esac; sleep 5
done
gh run view ${s#completed } -R PlayHQtv/Claude-Play --log | grep -o '{"public_id".*}' | sort -u
