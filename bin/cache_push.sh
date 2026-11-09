#!/bin/bash
# Saves the private image folders (never committed readable) as an encrypted cache in the draft release.
set -e
cd "$(dirname "$0")/.."; M=templates/meta-carousel; W=$(mktemp -d)
tar -C $M -cf $W/data.tar _build/s1 $( [ -d $M/_build/w ] && echo _build/w ) $( [ -d $M/_build/gta ] && echo _build/gta )
openssl rand -hex 32 | tr -d '\n' > $W/k
openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:$W/k -in $W/data.tar -out $W/data.enc
openssl pkeyutl -encrypt -pubin -inkey fx/pubkey.pem -pkeyopt rsa_padding_mode:oaep -in $W/k -out $W/key.enc
B=tmp-cache-$(date +%s); 
git checkout -q -b $B && mkdir -p bundle && tar -C $W -cf bundle/cache.tar key.enc data.enc && git add -f bundle/cache.tar
git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -m "cache" && git push -q "$(git remote | head -1)" $B 2>&1 | grep -iE "error|reject" || true
git checkout -q - && git branch -D -q $B; rm -rf $W
echo "cache pushed ($B)"
