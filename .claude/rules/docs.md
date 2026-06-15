# Docs & README guidelines

Generic rules for writing and updating documentation in this and any
repo I work on with you.

## When to touch docs

**Create or update only when:**

* The user explicitly asks for it.
* A code change makes existing docs factually wrong (broken command,
  renamed flag, removed endpoint) — fix the doc in the same commit as
  the code, scoped to exactly what broke.

**Never:**

* Create a README, CHANGELOG, or any `.md` file speculatively.
* Add inline code comments that restate what the code already says.
* Generate architecture diagrams, ADRs, or wikis unless asked.
* Touch docs as part of a refactor that has no user-visible behaviour
  change.

## File placement

| Doc type          | Location                        |
|-------------------|---------------------------------|
| Project overview  | `README.md` (repo root)         |
| Module/component  | `docs/<topic>.md` or inline     |
| API reference     | `docs/api.md`                   |
| Runbooks / ops    | `docs/runbook-<name>.md`        |
| Architecture      | `docs/architecture.md`          |
| Changelog         | `CHANGELOG.md` (root)           |

Never write working files, notes, or scratch docs to the repo root.

## README structure

A README should answer exactly four questions, in order:

1. **What is this?** — one or two sentences, no jargon.
2. **How do I run it?** — minimal prerequisites + quickstart commands.
3. **How do I configure it?** — required env vars / config keys only;
   link to a fuller reference if needed.
4. **How do I contribute / extend it?** — only if the project is
   collaborative or open-source.

Omit any section that has nothing to say. A short README is better
than a padded one.

## Style

* Write in plain English. Prefer short sentences.
* Use second person ("run `idf.py build`", not "the user should run").
* Use present tense ("returns a frame", not "will return a frame").
* Lead each section with what the reader needs to *do*, not what the
  system *is*.
* Use fenced code blocks with a language tag for every snippet.
* Keep line length ≤ 80 characters in prose; no limit inside code blocks.
* No trailing whitespace. No more than one blank line between sections.

## What belongs in docs vs code

| Belongs in docs                         | Belongs in code (or nowhere) |
|-----------------------------------------|------------------------------|
| How to build, flash, deploy             | What a function does         |
| Required hardware / wiring              | Variable names               |
| Environment variables and their meaning | Obvious control flow         |
| Known limitations / caveats             | TODO lists                   |
| External dependencies and why           | Change history               |

## Updating existing docs

* Edit the minimum needed — don't rewrite sections unrelated to your
  change.
* If a command or path changes, update every occurrence in the same
  commit.
* Delete stale content rather than leaving it with a "deprecated"
  label.
* Keep examples runnable. If an example would break with the current
  code, fix it or remove it.

## Commit rules for docs

Follow `commits.md`. Use type `docs` for pure documentation commits.
Scope to the file or area changed:

```
docs(readme): update flash command for ESP-IDF v5
docs(api): add upload endpoint request/response shape
docs: remove stale nmcli setup section
```

A `docs` commit must contain **only** documentation changes. If you
are fixing a doc that broke because of a code change, include the doc
fix in the same commit as the code change and use the code's type
(`fix`, `feat`, etc.), not `docs`.

## What NOT to write

* Personal opinions on design decisions (unless asked for an ADR).
* Step-by-step tutorials for well-documented third-party tools — link
  instead.
* Timestamps, author names, or "last updated" lines — git blame covers
  that.
* Badge soup (CI status, coverage, license) unless the project is
  public and they are kept up to date automatically.
