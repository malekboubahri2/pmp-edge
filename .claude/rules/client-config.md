# Building a Client Config From What You Learn

As you work on a client's projects you learn durable facts — their brand, their
stack choices, their domain vocabulary, their conventions, their gotchas.
**Capture the client-specific ones into that client's overlay** so the next
project for them starts already knowing it. Keep the generic ones in `base/`.
This is how this config compounds over time instead of being re-derived.

## Two layers, one test

- **`base/`** = generic. True for *any* client or project.
- **`clients/<client>/`** = specific to one client/org.

Before recording a learning, ask: **"Would this be just as true for a different
client?"** Yes → it belongs in `base/`. No → it belongs in that client's overlay.

## What lives in a client overlay

```
clients/<client>/
├── CLAUDE.md                     # client profile: who they are, defaults, per-project stub
├── .claude/rules/
│   ├── visual-identity.md        # brand: color, type, components, anti-patterns
│   ├── tech-stack.md             # preferred / locked stack (and the why)
│   └── <domain>.md               # domain vocabulary, conventions, recurring "do NOT"s
└── assets/                       # themes, logos, fonts, anything binary the brand needs
```

## When to capture (triggers)

Record it the moment you notice something that will also be true on the client's
**next** project:

- a brand/visual decision — a color, a font, a spacing rule, an anti-pattern;
- a locked tech choice — and the reason / ADR behind it;
- domain vocabulary and naming conventions the client uses;
- an environment or deploy specific — target hardware, hostname pattern, locale;
- a hard-won lesson — "on this client's stack, do NOT …".

One-off, project-only facts do **not** go here — they live in that project's own
`CLAUDE.md` or in session memory.

## How to capture

1. **Decide the layer** with the test above. If it's generic, improve `base/`
   instead — don't bury a universal lesson inside one client.
2. **Bootstrap if needed.** If the client has no overlay yet, create
   `clients/<client>/` by copying the structure of an existing one (e.g.
   `clients/pmp/`) and replacing its content.
3. **Record it concisely** in the right file. Update an existing entry rather
   than duplicating; supersede a stale one rather than leaving it.
4. **Keep profiles short and current** — they're read at the start of every
   session for that client.
5. **Commit it** (Conventional Commit) so it's shared and versioned. Promote
   durable client facts *out of* session memory into the overlay — memory is
   per-machine and transient; the committed overlay is the shared source of truth.

## Don'ts

- Don't put project-only specifics in a client overlay (they belong in that
  project's `CLAUDE.md`).
- Don't duplicate `base/` inside an overlay — an overlay only *adds* the
  client's specifics.
- Don't let an overlay drift; when you find it wrong, fix it in the same change.
