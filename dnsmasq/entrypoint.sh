#!/bin/sh
# Generate dnsmasq config from env, then run it in the foreground.
#
# One wildcard record (`address=/<base>/<ip>`) resolves the base domain AND
# every subdomain to this Pi. New apps just pick a subdomain — no DNS edit.
#
# Trade-off vs the old per-name `interface-name`: `address=` pins the IP read at
# container start, so a mid-run DHCP change needs a `docker compose restart dns`
# (or a DHCP reservation — recommended anyway).
set -eu

BASE_DOMAIN="${BASE_DOMAIN:-pmp.lan}"
UPSTREAM="${UPSTREAM_DNS:-1.1.1.1}"

# Pin the LAN interface with LAN_IFACE, else auto-detect the default-route one.
if [ -z "${LAN_IFACE:-}" ]; then
    LAN_IFACE="$(ip route get 1.1.1.1 2>/dev/null | sed -n 's/.* dev \([^ ]*\).*/\1/p' | head -n1)"
fi
LAN_IFACE="${LAN_IFACE:-eth0}"

# Current IPv4 of that interface — the wildcard target.
LAN_IP="$(ip -4 addr show "$LAN_IFACE" 2>/dev/null | sed -n 's/.*inet \([0-9.]*\).*/\1/p' | head -n1)"
if [ -z "${LAN_IP:-}" ]; then
    echo "dnsmasq: could not read an IPv4 on ${LAN_IFACE}" >&2
    exit 1
fi

cat > /etc/dnsmasq.conf <<EOF
# Generated at container start from env — edit BASE_DOMAIN / LAN_IFACE /
# UPSTREAM_DNS on the service instead of this file.
port=53
no-resolv
no-hosts
server=${UPSTREAM}
interface=${LAN_IFACE}
bind-dynamic
# Wildcard: ${BASE_DOMAIN} and every *.${BASE_DOMAIN} → this Pi.
address=/${BASE_DOMAIN}/${LAN_IP}
EOF

echo "dnsmasq: *.${BASE_DOMAIN} -> ${LAN_IP} (${LAN_IFACE}); upstream ${UPSTREAM}"
exec dnsmasq --keep-in-foreground --log-facility=- --conf-file=/etc/dnsmasq.conf
