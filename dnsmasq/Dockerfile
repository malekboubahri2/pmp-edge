# Tiny DNS appliance for the plant LAN: a wildcard *.BASE_DOMAIN → this Pi.
#
# Host networking (set in compose) lets it read the live interface address and
# bind :53 on the LAN; a bridged container would only see its 172.x address.
FROM alpine:3.20

# iproute2 gives a full `ip` for default-route detection + reading the LAN IP.
RUN apk add --no-cache dnsmasq iproute2

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# dnsmasq binds :53 as root then drops privileges to the dnsmasq user itself.
ENTRYPOINT ["/entrypoint.sh"]
