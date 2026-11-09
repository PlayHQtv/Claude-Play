#!/bin/bash
# Downloads the ONNX vision models (BiRefNet, Segment Anything, Depth Anything V2) from public GitHub releases.
# They are never committed. "full" also fetches the large BiRefNet (needs ~10 GB RAM -> GitHub runner).
set -e
D=${PHQ_MODELS:-/tmp/models}; mkdir -p "$D"; R=https://github.com/danielgatis/rembg/releases/download/v0.0.0
get(){ [ -s "$D/$2" ] || curl -fsSL -o "$D/$2" "$1"; }
get $R/BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx BiRefNet-general-lite.onnx
get $R/vit_b-encoder-quant.onnx vit_b-encoder-quant.onnx
get $R/vit_b-decoder-quant.onnx vit_b-decoder-quant.onnx
get https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/v2.0.0/depth_anything_v2_vits.onnx depth_anything_v2_vits.onnx
get https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx yunet.onnx
[ "$1" = full ] && get $R/BiRefNet-general-epoch_244.onnx BiRefNet-general-epoch_244.onnx
ls -la "$D"
