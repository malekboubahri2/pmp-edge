#!/usr/bin/env bash
# Generate the vendor signing keypair (Ed25519). Run ONCE, on your own machine.
#
#   bash tools/gen-keys.sh
#
# - private.pem  → KEEP SECRET, never put it on the Pi. Used to mint licenses.
# - public.pem   → install on the Pi at license/secrets/public.pem (the gate verifies with it).
set -euo pipefail

OUT="${1:-.}"
openssl genpkey -algorithm ed25519 -out "$OUT/private.pem"
openssl pkey -in "$OUT/private.pem" -pubout -out "$OUT/public.pem"
chmod 600 "$OUT/private.pem"

echo "Wrote:"
echo "  $OUT/private.pem  (SECRET — keep off the Pi; back it up safely)"
echo "  $OUT/public.pem   (install on the Pi: license/secrets/public.pem)"
