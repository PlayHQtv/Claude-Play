#!/bin/bash
# Saves the private image folders (never committed readable) as an encrypted cache in the draft release.
# The encrypted data is split into 90 MB parts (GitHub refuses files > 100 MB – a single cache.tar silently
# failed to upload once it grew past that limit, 13.11.2026). demo_* (rejected layouts) stay out.
set -e
cd "$(dirname "$0")/.."; M=templates/meta-carousel; W=$(mktemp -d)
tar -C $M --exclude="_build/gta/demo_*" -cf $W/data.tar _build/s1 $( [ -d $M/_build/w ] && echo _build/w ) $( [ -d $M/_build/gta ] && echo _build/gta )
openssl rand -hex 32 | tr -d '\n' > $W/k
openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:$W/k -in $W/data.tar -out $W/data.enc
openssl pkeyutl -encrypt -pubin -inkey fx/pubkey.pem -pkeyopt rsa_padding_mode:oaep -in $W/k -out $W/key.enc
B=tmp-cache-$(date +%s)
git checkout -q -b $B && mkdir -p bundle/cache && cp $W/key.enc bundle/cache/cache_key.enc && split -b 90M -d -a 2 $W/data.enc bundle/cache/cache_part
git add -f bundle/cache && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -m "cache"
if ! git push -q "$(git remote | head -1)" $B; then git checkout -q - ; git branch -D -q $B; rm -rf $W; echo "CACHE PUSH FAILED" >&2; exit 1; fi
git checkout -q - && git branch -D -q $B; echo "cache pushed ($B, $(ls bundle/cache 2>/dev/null | wc -l) files, $(du -h $W/data.enc | cut -f1))"; rm -rf $W bundle/cache
