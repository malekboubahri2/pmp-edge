# Engineering Principles

Universal principles for **any** project — a web app, a CLI, a library, a data
pipeline, a service, firmware. They outrank convenience: if a proposed solution
violates one, say so and propose an alternative rather than silently complying.
Language- and domain-agnostic; apply them through each ecosystem's idioms.

---

## 1. Modularity & single responsibility

Extra files are fine; tangled responsibilities are not. Every unit (module,
function, class, package) owns **one** concern, exposes a narrow interface, and
knows nothing about its callers. If you cannot state a unit's responsibility in
one sentence, it is too big — split it.

- One concept per file; a small public surface, the rest private.
- No circular dependencies. Dependencies point one way: higher-level depends on
  lower-level, never the reverse.
- Cross-cutting concerns (logging, config, time, randomness) are **injected**,
  not reached into from business logic.

*Payoff:* when a requirement moves, the blast radius is one unit.

---

## 2. Portability — no environment coupling

The same code runs on a developer machine, CI, and the target unchanged.

- No hardcoded paths, hosts, ports, credentials, or absolute assumptions in
  source. Configuration comes from environment, config files, or arguments.
- Isolate platform/vendor specifics behind an abstraction so the core is
  testable without them (a fake or mock stands in).
- A new environment should be a config change, never a code change.

---

## 3. Clear contracts, one source of truth

Build for the *next* caller without over-building for it.

- Stable, documented interfaces between components; **version** anything other
  programs depend on (an API, a file format, a message schema, a public type).
- **One source of truth per concern.** Find the single place a thing happens and
  route every caller through it — never branch the same logic per caller,
  transport, or platform.
- Don't repeat knowledge; but don't abstract on first sight either (see #4).
- Explicit over clever. No magic. A reader should predict behavior from the name.

---

## 4. Simplicity first; flexibility only at the seams (YAGNI)

The cheapest code is the code you didn't write. Solve today's problem well.

- Prefer the simplest design that meets the requirement. Add a layer only when a
  second concrete need exists, not on speculation.
- Where change is genuinely likely, design a **seam** (an interface) or a
  **flag** so the future change is contained — but defer building the future
  behavior until it's needed.
- Delete dead code and unused options. Optionality has a carrying cost.

---

## 5. Idiomatic to the language & ecosystem

Good structure in Python differs from Go, from TypeScript, from C. Follow the
conventions native to the stack; don't import patterns from one onto another.

- Use the ecosystem's standard project layout, dependency manager, test runner,
  and formatting/lint tools.
- Match the surrounding code's style, naming, and density — new code should read
  as if it was already there.

---

## Cross-cutting habits

- **Validate input at boundaries.** Trust nothing crossing a process, network,
  or user edge; validate once, at the edge, then trust it inside.
- **Fail loudly and early.** Surface errors where they occur with context;
  don't swallow them or paper over a broken state.
- **Make state explicit.** Avoid hidden global mutable state; if it's
  unavoidable, document it and provide a reset path for tests.
- **Security and time, by default.** Never log or commit secrets; validate and
  least-privilege at trust boundaries. Time is UTC on the wire, local only at
  the presentation edge.

---

## Using these

- Cite a principle by number when you push back on a request.
- When two principles conflict (e.g. one-source-of-truth vs YAGNI), record the
  resolution where the project keeps decisions.
- These are stable. Change them deliberately, and update this file when you do.
