#!/bin/bash
# Restores the private image folders from the encrypted cache (after a fresh checkout / environment reset).
set -e
cd "$(dirname "$0")/.."; M=templates/meta-carousel; W=$(mktemp -d); R=repos/PlayHQtv/Claude-Play
for rid in $(gh api "$R/releases" -q '.[]|select(.name=="grab-private")|.id'); do
  for n in cache.tar fx_key_v2.pem; do id=$(gh api "$R/releases/$rid/assets?per_page=100" -q ".[]|select(.name==\"$n\")|.id"); [ -n "$id" ] && gh api -H "Accept: application/octet-stream" "$R/releases/assets/$id" > $W/$n; done
done
tar -C $W -xf $W/cache.tar
openssl pkeyutl -decrypt -inkey $W/fx_key_v2.pem -pkeyopt rsa_padding_mode:oaep -in $W/key.enc -out $W/k
openssl enc -d -aes-256-cbc -pbkdf2 -pass file:$W/k -in $W/data.enc | tar -C $M -x
rm -rf $W; echo "cache restored: $(ls $M/_build/s1 | wc -l) files"
