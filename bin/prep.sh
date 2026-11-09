#!/bin/bash
# prep.sh <renderer> <data.json> <tag> [slides e.g. "1 3"]  ->  render (3x) + QA (abort on ERROR) + upload dir /tmp/up_<tag>/<tag>_NN.jpg
# Then: sign the printed public_ids, run bin/signed.py, bin/bundle.sh /tmp/up_<tag>
set -e
cd "$(dirname "$0")/../templates/meta-carousel"; R=$1; D=$2; T=$3; S=${4:-}
O=/tmp/out_$T; U=/tmp/up_$T; rm -rf $O $U; mkdir -p $U
python3 -c "import spellchecker, cv2" 2>/dev/null || pip install -q --break-system-packages pyspellchecker opencv-python-headless >/dev/null 2>&1
python3 dupcheck.py $D | sed 's/^/dup: /' || echo "dup: WARNING - cover hero image was already used in an earlier post (pick another unless intended)"
python3 $R.py $D $O >/dev/null 2>&1
python3 qa.py $O > $O.qa 2>/dev/null && rc=0 || rc=$?; grep -E "^QA|ERROR|contrast|unknown words" $O.qa; [ $rc = 0 ] || { echo "QA ERROR - stop"; exit 1; }
i=0; for f in $(ls $O/*.jpg | sort); do i=$((i+1)); if [ -z "$S" ] || [[ " $S " == *" $i "* ]]; then cp $f $U/${T}_$(printf %02d $i).jpg; fi; done
echo "to sign:"; ls $U | sed "s#^#playhq/tmp/#; s#\.jpg##"
