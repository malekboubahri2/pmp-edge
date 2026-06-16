# Activation / grace gate

An **optional, reversible** way to deploy apps behind pmp-edge *before payment*:
they run normally during an evaluation window, then show a polite **"Activation
required"** page until you (the vendor) drop in a signed license. **No data is
ever touched** — it's a gate at the proxy, not a kill-switch.

It's a generic edge feature (tenant activation), not tied to any one client.

## How it works

```
client ──▶ edge proxy ──forward_auth──▶ license sidecar ──▶ verify signed token
                 │                              │
                 │  204 (active/grace) ─────────┘  → request proceeds to the app
                 └─ 402 + activation page  ─────────  (token missing/expired/invalid)
```

- A **license sidecar** (`license/`) holds your **public** key and a **signed
  license token**. On every request Caddy calls its `/verify`:
  - **active / grace** → `204` → the app is served.
  - **expired / missing / invalid / clock-rolled-back** → `402` + a branded
    activation page.
- The token is a **JWT signed with your PRIVATE key** (kept off the Pi), so the
  client can't forge or extend it. To unlock: issue a new token and replace the
  file — the next request picks it up, **no restart, no data change**.
- **Per-app opt-in:** an app is gated only if its web container carries the
  `caddy.forward_auth` labels (see `examples/app-on-edge.yml`).

## One-time setup (on your machine)

```bash
bash tools/gen-keys.sh           # → private.pem (SECRET, keep off the Pi) + public.pem
pip install "pyjwt[crypto]"      # for issuing tokens
```

Install on the Pi (gitignored, provisioned out-of-band):
```
pmp-edge/license/secrets/public.pem      ← copy public.pem here
pmp-edge/license/secrets/token.jwt       ← the current license (see below)
```

Set the activation-page contact in the edge `.env`:
```
VENDOR_NAME=Your Company
VENDOR_CONTACT=you@example.com
```

## Issue / renew a license

```bash
# evaluation: 30 days, banner in the last 14
python tools/issue_license.py --key private.pem --sub pmp --days 30 --grace 14 > token.jwt
scp token.jwt user@<pi>:~/pmp-edge/license/secrets/token.jwt
```

- **On payment:** re-run with a long window (e.g. `--days 3650`) and replace
  `token.jwt`. Unlocks instantly.
- **To lock now:** delete `token.jwt` (or let it expire) → the gate fails closed.

## Gate an app

Add to the app's web-container labels (alongside the `caddy:` hostname label):
```yaml
caddy.forward_auth: license:8080
caddy.forward_auth.uri: /verify
```
Both the app's container and the `license` sidecar are on the shared `edge`
network, so `license:8080` resolves. Verify the generated routing with:
```bash
docker compose -p pmp-edge exec proxy cat /etc/caddy/Caddyfile
```

## Grace banner (optional)

`GET /status` returns `{ state, expires, days_left, sub }`. Expose it through the
edge (or have apps query it) to show a "evaluation ends in N days" banner before
lockdown. Left to the app — the gate itself only does the hard block.

## Design notes & limits

- **Reversible + non-destructive by design.** Never delete data or brick the box.
  At expiry the app is *gated*, not damaged.
- **Fails closed.** No/invalid token ⇒ locked. So a license sidecar outage gates
  the apps too — keep it simple and healthchecked (it is). Weigh this vs. the
  risk of a paid client being locked by a sidecar bug.
- **Clock-rollback resistance:** a high-water-mark on a volume; setting the clock
  back more than `LICENSE_ROLLBACK_SKEW_SEC` (default 2 days) locks as tampered.
- **It's friction, not DRM.** The client has root/Docker on the Pi and can remove
  the gate — but doing so means tampering with the ingress (DNS/TLS/routing) and
  is an obvious, deliberate act. The **contract is the real protection**; this is
  the polite, auditable backstop.
- **Disclose it.** Put the evaluation/activation terms in the deployment
  agreement. A disclosed, reversible activation gate is legitimate; a hidden
  destructive trap is not — and would undermine you legally and commercially.
