#!/bin/bash
# Restores the private image folders from the encrypted cache (after a fresh checkout / environment reset).
# New format: cache_key.enc + cache_part00.. (split, see cache_push.sh); old format cache.tar as fallback.
set -e
cd "$(dirname "$0")/.."; M=templates/meta-carousel; W=$(mktemp -d); R=repos/PlayHQtv/Claude-Play
rid=$(gh api "$R/releases" -q '.[]|select(.name=="grab-private")|.id' | while read r; do n=$(for pg in 1 2 3 4; do gh api "$R/releases/$r/assets?per_page=100&page=$pg" -q 'length'; done | paste -sd+ | bc); echo "$n $r"; done | sort -rn | head -1 | cut -d' ' -f2)
for pg in 1 2 3 4; do gh api "$R/releases/$rid/assets?per_page=100&page=$pg" -q '.[]|(.id|tostring)+" "+.name'; done > $W/list
get(){ id=$(awk -v n="$1" '$2==n{print $1}' $W/list | head -1); [ -n "$id" ] && gh api -H "Accept: application/octet-stream" "$R/releases/assets/$id" > "$W/$1"; }
get fx_key_v2.pem
if grep -q " cache_key.enc$" $W/list; then
  get cache_key.enc; mv $W/cache_key.enc $W/key.enc
  for p in $(awk '$2 ~ /^cache_part[0-9][0-9]$/ {print $2}' $W/list | sort); do get $p; cat $W/$p >> $W/data.enc; rm $W/$p; done
else
  get cache.tar; tar -C $W -xf $W/cache.tar
fi
openssl pkeyutl -decrypt -inkey $W/fx_key_v2.pem -pkeyopt rsa_padding_mode:oaep -in $W/key.enc -out $W/k
openssl enc -d -aes-256-cbc -pbkdf2 -pass file:$W/k -in $W/data.enc | tar -C $M -x
rm -rf $W; echo "cache restored: $(ls $M/_build/s1 | wc -l) s1 + $(ls $M/_build/gta | wc -l) gta files"
