# Way of Working — how to approach any build

How to *think* when building or changing software on this account, for any kind
of project. Read it as reasoning, not a checklist. It pairs with
`principles.md` (the *why*), `commits.md`, and `docs.md`.

---

## 0. The one-line philosophy

> Build the smallest thing that proves the point, behind clean interfaces, so
> the next change is contained. Understand first, verify always, claim nothing
> without evidence.

---

## 1. Understand before you build

- Read the relevant context first: the project's own `CLAUDE.md`, the **nearest
  sibling file**, and any recalled memory. Match the existing structure, naming,
  and idiom — new code should look like it was already there.
- **Verify a recalled or assumed fact before acting on it** (files move, flags
  get renamed, APIs change).
- Find the one place a concern already lives before adding a second.

---

## 2. Plan in proportion to the change

- For anything touching several files or making a hard-to-reverse choice, form a
  short plan first.
- Ask **one** clarifying question only on a genuine fork in the road — not three,
  and not for choices with an obvious default. When you can act, act.
- For a one-line fix, just do it.

---

## 3. Thinnest slice first; defer the hard edges

- Get one path working **end to end on real data** — real input → real
  processing → real output — before widening it.
- Then widen: more cases, more configuration, more polish.
- **Defer the hard edges** (offline, scale, exotic inputs, lockdown) until the
  core idea is proven. They're real work, but they don't validate the idea, so
  they don't go first.
- During a migration, keep the old path alive — no big-bang cutovers.

---

## 4. Record decisions that are expensive to reverse

- When you make a choice that's costly to undo (a data model, a public contract,
  a dependency, a security trade-off), write a short decision record: context,
  decision, trade-off — the *why*, not the how.
- When a decision changes, **supersede it with a new record**; don't rewrite
  history. The old record is the memory of what was once true.

---

## 5. One contract per concern

- Never branch the same business logic per caller, transport, or platform. Route
  every caller through one implementation behind one interface.
- Keep contracts **versioned and documented** so adding a caller or an
  integration is additive, not invasive.
- Design the seam for a likely future need now (cheap); build the feature only
  when it's needed (YAGNI).

---

## 6. Make change cheap — but only where it pays

- Use a **flag** or **config** where behavior will genuinely toggle or differ by
  environment, so changing it is a config change, not a code change.
- Put platform/vendor specifics behind an abstraction so swapping them is
  contained.
- Don't pre-build flexibility you can't name a second use for.

---

## 7. Verify; never claim done without evidence

- Run the typecheck/lint/tests after a change. **A successful build is a real
  gate** — if the test runner is flaky, fall back to a clean compile + build and
  say that's what you did.
- For anything deployed or run, **check the actual result**: the command exits
  clean, the output is what you expected, the service answers, the change is
  present where it should be.
- Report honestly. Show failing output. Name skipped steps. Don't hedge when it
  works; don't claim it when it doesn't.

---

## 8. Commit and document with discipline

- **Conventional Commits**, small and atomic, ordered so a reader can follow the
  work (`commits.md`). If the subject needs "and", split the commit.
- **Docs only when asked, or when a code change makes a doc wrong** (`docs.md`).
  Fix the broken doc in the same commit as the code. No speculative files, no
  comments that restate the code.
- **Never commit secrets.** Keep `.env` gitignored; document keys in
  `.env.example`. Push and deploy only when asked; treat `main` as protected.

---

## 9. Spend effort in proportion

- Match the depth of work to the task. A small fix doesn't need a plan, a swarm,
  or a doc. A cross-cutting change does.
- Don't re-derive context you already have, re-litigate a settled decision, or
  enumerate options you won't take. Recommend, then proceed.

---

## 10. Carry knowledge across sessions

- Persist **non-obvious** facts (decisions not visible in code, gotchas,
  environment quirks) to memory; convert relative dates to absolute. Don't
  persist what the repo already records.
- Update or delete a memory when it changes or proves wrong.

---

## The shape of a good session

1. Read context (project `CLAUDE.md`, sibling files, memory); verify assumptions.
2. Plan in proportion; ask one question only on a real fork.
3. Thinnest end-to-end slice first; widen; defer the hard edges.
4. Record any expensive decision.
5. One contract per concern; flags/abstractions only where they pay.
6. Verify (typecheck/build/tests; check the real result).
7. Atomic Conventional commit; docs only if owed.
8. Persist what was non-obvious to memory.
