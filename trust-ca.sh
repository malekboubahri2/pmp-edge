#!/usr/bin/env bash
# Export pmp-edge's internal-CA root certificate so you can install it on client
# devices. Trust it once and HTTPS to every app on the Pi is trusted.
#
#   bash trust-ca.sh [output-file]      # default: pmp-edge-ca.crt
set -euo pipefail

OUT="${1:-pmp-edge-ca.crt}"

docker compose -p pmp-edge cp \
  proxy:/data/caddy/pki/authorities/local/root.crt "$OUT"

echo "Wrote $OUT"
echo "Install it on each client (see README → 'Trust the CA')."
