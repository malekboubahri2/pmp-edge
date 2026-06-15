# PMP Preferred Tech Stack

> **Client overlay (PMP).** The default stack for a PMP project. Once chosen for
> a project it is **locked** — change it only via an Architecture Decision
> Record. Prune what a given project doesn't need (e.g. drop firmware/MQTT for a
> pure web tool). The bias: a few boring, proven tools that run identically on a
> laptop, CI, and the target, all in containers.

## Server

| Choice | Why |
|---|---|
| Python 3.11+, FastAPI + Uvicorn | Async, typed, OpenAPI for free; one backend language only |
| SQLAlchemy 2.0 + Alembic | Typed ORM; migrations are the *only* way the schema changes |
| SQLite (WAL) → Postgres if scale demands | Zero-ops for a PoC; the swap is an ADR |
| JWT + argon2 | Standard bearer auth; argon2 for password/secret hashing |
| paho-mqtt + Mosquitto | Only if the project has devices/telemetry; else omit |
| pytest, Docker | Fast tests; the container is the unit of deployment |

**Structure:** thin routers → services (own transactions + side effects) →
models → db. One Pydantic schema per direction (`Create`/`Update`/`Read`). No
SQL or business logic in routers.

## Dashboard / web

| Choice | Why |
|---|---|
| React + TypeScript + Vite | Fast HMR, typed, team default |
| TailwindCSS + shadcn/ui | Brand tokens as theme; accessible primitives |
| TanStack Query | Server state in a cache, not Redux; SSE/poll invalidation |
| React Router | Routing + auth guards |
| Zod + react-hook-form | Validation at the boundary, typed forms |
| Recharts | Charts that match the brand palette |
| PWA (service worker + IndexedDB) | When a kiosk/offline surface is needed |
| Docker multi-stage → Caddy | One built bundle, TLS-terminated by Caddy |

**The web surface is the product's selling point for PMP** — invest in
interactivity, animation, polish. Feature-sliced architecture; keep
motion/interaction primitives in `lib/` so polish never leaks into business
logic. Apply `visual-identity.md` and `assets/theme.css`.

## Firmware (embedded projects only)

| Choice | Why |
|---|---|
| STM32CubeIDE + CubeMX (HAL) | Vendor toolchain; generated HAL |
| TouchGFX | Rich touch UI; MVP (View renders / Presenter decides / Model holds state) |
| FreeRTOS (CMSIS-RTOS2) | Tasks, sane concurrency |
| Network behind a HAL | Pluggable transport; no networking in business logic; no dynamic allocation in steady state |

## Infra

| Choice | Why |
|---|---|
| Docker Compose (dev + prod) | Same stack, different `.env` |
| Caddy | Reverse proxy + automatic TLS (internal CA for LAN kiosks) |
| Mosquitto | MQTT broker — only if devices exist |
| dnsmasq (optional) | Friendly LAN hostname → the box's current DHCP IP |
| Multi-arch images (`amd64` + `arm64`) | Dev laptop + Raspberry Pi / ARM target |

## Hard rules

- One backend language (Python). One package manager per ecosystem (uv, pnpm).
- Everything server-side is a container; non-root runtime, healthchecks, named
  volumes for state.
- UTC on the wire; local time only in the UI. Default UI locale `fr-TN` (PMP
  operates in French).
- Semver per component; `main` always deployable; no hardcoded IPs/hosts/ports;
  no committed secrets.
