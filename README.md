# pmp-edge

Shared **ingress** for every app on the Pi: one reverse proxy (Caddy) and one
DNS server (dnsmasq). Deploy it once; apps become tenants that just join a
network and declare a hostname. No more port clashes, no per-app DNS or TLS.

## Why

Running several full stacks on one host (qc_system, qc_level_1, future apps)
means they fight over `:80`, `:443`, `:53` and each ships its own Caddy/CA.
`pmp-edge` owns those once and routes by **hostname** to each app:

```
                       pmp-edge
 clients ──DNS:53────▶  dnsmasq   *.pmp.lan → Pi's live IP (one wildcard)
 browser ──:80/:443──▶  Caddy     Host → app container on the `edge` network
                          │ edge network (shared, external)
        ┌─────────────────┼──────────────────┬───────────────────┐
   qc_system          qc_level_1          future-app …      (no host ports;
   inspection.pmp.lan  qcl1.pmp.lan        app3.pmp.lan       labels only)
```

- **One DNS record.** `*.pmp.lan` → the Pi. New app = pick a subdomain, no DNS edit.
- **One CA.** Caddy's internal CA signs every hostname; install it on clients once.
- **No port clashes.** Only the edge binds `:80/:443/:53`; apps publish nothing.

## Deploy (first, before any app)

```bash
cp .env.example .env          # set BASE_DOMAIN, UPSTREAM_DNS
docker compose -p pmp-edge up -d --build
```

This creates the external **`edge`** network and starts the proxy + DNS.

## Connect an app

In the app's own `docker-compose.yml` (see `examples/app-on-edge.yml`):

1. Join the external `edge` network.
2. Remove any `ports:` that publish 80/443.
3. Add labels to the web container:

```yaml
networks:
  edge: { external: true, name: edge }
  internal: {}
services:
  web:
    networks: [edge, internal]
    labels:
      caddy: qcl1.pmp.lan
      caddy.reverse_proxy: "{{upstreams 80}}"
      caddy.tls: internal
  api:
    networks: [internal]      # stays private
```

Then `docker compose -p qc_level1 up -d`. The proxy notices the labels and the
app is live at `https://qcl1.pmp.lan` — no edge or DNS changes. Removing the app
(`down`) removes its route automatically.

Verify the generated routing:
```bash
docker compose -p pmp-edge exec proxy cat /etc/caddy/Caddyfile
```

## DNS — point clients at the Pi

Names only resolve if devices ask the Pi's dnsmasq. Pick one:

- **Router DHCP** → primary DNS = the Pi (best; every device gets every app).
- **Per device** → static DNS = the Pi.
- **hosts file** (desktops) → `<pi-ip> qcl1.pmp.lan` (one line per app; Android needs root).

`UPSTREAM_DNS` forwards all other lookups, so internet/LAN names keep working.
Give the Pi a **DHCP reservation** so its IP is stable.

## Trust the CA

Caddy uses an internal CA (no public ACME on a closed LAN). Export and install
it once per client:

```bash
bash trust-ca.sh                 # writes pmp-edge-ca.crt
```

- **Windows:** import into *Trusted Root Certification Authorities*.
- **Linux:** `sudo cp pmp-edge-ca.crt /usr/local/share/ca-certificates/ && sudo update-ca-certificates`
- **Android:** Settings → Security → Encryption & credentials → Install a CA certificate.

Plain `http://<app>.pmp.lan` also works (HTTP→HTTPS redirect is disabled), which
is handy for wall displays that don't need TLS.

## Migrating the existing apps

1. Bring up `pmp-edge` (creates the `edge` network).
2. **Move DNS here:** stop qc_system's own `dnsmasq`; this one replaces it with a
   wildcard. (Their fixed names still work — make them subdomains of `BASE_DOMAIN`,
   e.g. `inspection.pmp.lan`, `andon.pmp.lan`.)
3. Per app: drop the `ports:` publish, join `edge`, add the three labels. You can
   keep each app's internal Caddy (the edge just proxies the hostname to it) so
   qc_system's `/level3` + andon-host logic stays untouched, or fold it into
   labels later.
4. Repoint client DNS at the Pi; trust the edge CA once.

## Trade-offs

- **`caddy-docker-proxy`** (the proxy image) is a widely-used third-party build
  of Caddy that reads Docker labels. If you prefer vanilla Caddy, swap it for
  `caddy:2` with `import /etc/caddy/sites.d/*.caddy` and have each app drop a
  snippet file + reload — more explicit, but apps write files instead of labels.
- **Wildcard DNS** pins the Pi IP at container start; a mid-run DHCP change needs
  `docker compose -p pmp-edge restart dns`. A DHCP reservation avoids this.
- Use a **private** `BASE_DOMAIN` (`pmp.lan`, `pmp.internal`, `pmp`) — a wildcard
  under a real domain (e.g. `pmp.com`) would shadow the whole real domain on the
  LAN.

## Files

```
docker-compose.yml      proxy (caddy-docker-proxy) + dns (dnsmasq)
.env.example            BASE_DOMAIN, UPSTREAM_DNS, LAN_IFACE
dnsmasq/                wildcard *.BASE_DOMAIN → live Pi IP
examples/app-on-edge.yml  how an app's compose joins
trust-ca.sh             export the internal CA for clients
license/                activation/grace gate (signed-token verifier)
tools/                  vendor tooling: gen-keys.sh + issue_license.py
docs/activation.md      activation/grace design + how to issue/install licenses
```

## Optional: activation / grace gate

Deploy apps **before payment** with a reversible activation gate — they run for
an evaluation window, then show a polite "Activation required" page until you drop
in a vendor-signed license (no data touched, unlocks instantly). It's an opt-in
`forward_auth` check per app. See [`docs/activation.md`](docs/activation.md).
