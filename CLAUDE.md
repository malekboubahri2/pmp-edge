# Engineering Guidelines

> Auto-read by Claude Code. These are **generic** guidelines that shape how you
> work on **any** project here — web, CLI, library, service, data, embedded.
> They are not tied to a stack or a domain. Project-specific facts (what this
> repo is, its stack, its status) belong in a short section a project adds
> *below*; these guidelines stay generic underneath.

## How to work (the short version)

> Build the smallest thing that proves the point, behind clean interfaces, so
> the next change is contained. Understand first, verify always, claim nothing
> without evidence.

The full reasoning lives in the rules, which are also auto-read:

- **`.claude/rules/principles.md`** — the 5 engineering principles (modularity,
  portability, clear contracts, simplicity/YAGNI, idiomatic) + cross-cutting
  habits. They outrank convenience.
- **`.claude/rules/way-of-working.md`** — how to approach a build: understand
  first, plan in proportion, thinnest slice first, record expensive decisions,
  one contract per concern, verify before claiming done.
- **`.claude/rules/commits.md`** — Conventional Commits; small, atomic, ordered.
- **`.claude/rules/docs.md`** — docs only when asked or when code makes them
  wrong.
- **`.claude/rules/dev-environment.md`** — work inside the project's VS Code dev
  container (dev/test/run/build); the devcontainer config is the one source of
  truth for the toolchain.
- **`.claude/rules/client-config.md`** — how to distil what you learn about a
  client (brand, stack, conventions, gotchas) into a reusable `clients/<client>/`
  overlay, so the config compounds across projects.

## Non-negotiables (apply everywhere)

- **Read before you edit.** Match the nearest sibling's style and idiom.
- **No hardcoded paths, hosts, ports, or secrets** in source — config instead.
- **Use the project's VS Code dev container** for dev/test/run/build when one
  exists; declare new tooling in the devcontainer config, not on the host.
- **One source of truth per concern;** don't branch the same logic per caller.
- **Validate input at boundaries; fail loudly.**
- **Verify your work** (typecheck/build/tests; check the real result) and
  **report outcomes honestly.**
- **Never commit secrets;** never push or deploy unless asked; treat `main` as
  protected.
- **Simplicity first** — add abstraction only for a second concrete need (YAGNI).
- **Ask one clarifying question** on a genuine fork, not three; otherwise act.

## When helping, prefer

- Concrete code over explanation when the design is decided.
- Pointing at an existing file over generating a new one.
- The pattern in the nearest sibling file over a new pattern.
- Tests alongside non-trivial code.
- Surfacing a principle violation explicitly instead of working around it.

---

## PMP client profile

PMP — Peinture et Métallisation sur Plastique — a paint/finishing plant; the
software digitalizes and instruments plant operations. Plant floor,
French-speaking; brand voice is **industrial luxury** (deep teal, gold accents,
warm cream). PMP defaults unless a project says otherwise:

- **Stack:** see `.claude/rules/tech-stack.md` — FastAPI + SQLite + Docker
  server; React + Vite + Tailwind + shadcn dashboard; STM32/TouchGFX firmware
  when embedded; Caddy + Mosquitto + Compose infra.
- **Brand (UI projects):** see `.claude/rules/visual-identity.md` — cream/teal/
  gold, Inter + JetBrains-Mono-for-data, the gold focus ring; brand is a feature.
- **Locale & time:** UI in French (`fr-TN`); UTC on the wire, local only in the UI.
- **Deploy target:** a Raspberry Pi / ARM box on the plant LAN, full stack in
  Docker, reached over Caddy-terminated HTTPS.

---

## This project

- **What it is:** `pmp-edge` — the shared **ingress** for every app on the Pi:
  one reverse proxy (Caddy via `caddy-docker-proxy`) + one DNS server (dnsmasq).
  Apps join the external `edge` network and declare a hostname with Caddy labels;
  the proxy routes by Host. No UI, no app stack — pure infrastructure.
- **Stack:** Docker Compose · `lucaslorentz/caddy-docker-proxy` · dnsmasq
  (Alpine). No language toolchain and no dashboard, so the PMP UI stack and
  `theme.css`/`visual-identity` don't apply here.
- **Run:** `docker compose -p pmp-edge up -d --build` — deploy **first**; it
  creates the external `edge` network the apps attach to.
- **Status:** scaffolded; not yet cut over on the Pi (it takes over :80/:443/:53
  from the per-app stacks — a deliberate migration). See `README.md`.
- **Project don'ts:** don't publish app host ports here; don't run a second DNS
  or proxy on the host; keep `BASE_DOMAIN` a **private** suffix — a wildcard
  under a real domain (e.g. `pmp.com`) shadows the whole domain on the LAN.

The generic guidelines above and the rules keep applying underneath this.
