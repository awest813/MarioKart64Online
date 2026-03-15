#!/usr/bin/env bash
# build_wasm.sh — Build MarioKart 64: Recompiled for WebAssembly via Emscripten.
#
# Prerequisites:
#   1. Emscripten SDK activated in the current shell:
#        source /path/to/emsdk/emsdk_env.sh
#   2. The recompiler output files already generated (see BUILDING.md steps 1-3).
#   3. cmake and ninja available on $PATH.
#
# Usage:
#   ./build_wasm.sh [Release|Debug]
#
# Output:
#   build-wasm/MarioKart64Recompiled.{html,js,wasm}

set -euo pipefail

BUILD_TYPE="${1:-Release}"
BUILD_DIR="build-wasm"

echo "==> Configuring Emscripten build (${BUILD_TYPE})…"
emcmake cmake \
  -S . \
  -B "${BUILD_DIR}" \
  -G Ninja \
  -DCMAKE_BUILD_TYPE="${BUILD_TYPE}"

echo "==> Building…"
cmake --build "${BUILD_DIR}" \
  --target MarioKart64Recompiled \
  -j"$(nproc 2>/dev/null || sysctl -n hw.logicalcpu 2>/dev/null || echo 4)" \
  --config "${BUILD_TYPE}"

echo ""
echo "Build complete.  Output files:"
ls -lh "${BUILD_DIR}/MarioKart64Recompiled.html" \
       "${BUILD_DIR}/MarioKart64Recompiled.js"   \
       "${BUILD_DIR}/MarioKart64Recompiled.wasm"  2>/dev/null || true
echo ""
echo "To serve locally (COOP/COEP headers required for SharedArrayBuffer / pthreads):"
echo "  cd ${BUILD_DIR} && python3 ../src/wasm/server.py"
echo "Then open http://localhost:8080/MarioKart64Recompiled.html in a browser."
