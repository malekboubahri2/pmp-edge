# Development Environment — VS Code Dev Containers

Generic rule for **any** project here. The development environment is a
**portability** concern (`principles.md` #2) and a **one source of truth**
concern (#3): the toolchain a project needs should be declared once, in version
control, and be identical on every machine and in CI.

## Default: work inside the dev container

When a repo has a `.devcontainer/`, do **dev, test, run, build, and lint inside
that container** — reopen the folder in the container and run commands there, not
on the host shell.

*Why:* the container pins the language runtime, system libraries, CLIs, and
editor extensions a project assumes. Working inside it means your results match
CI and every teammate — no "works on my machine", no host drift, no polluting
the host with project-specific toolchains.

## The devcontainer config is the single source of truth

`.devcontainer/devcontainer.json` (plus its `Dockerfile` / `compose.yaml`) is
the one place the dev toolchain is declared.

- Need a tool, runtime version, service, or extension? **Add it to the
  devcontainer config**, not ad hoc on the host. A new dependency is a config
  change, committed — never a manual "install this first" step.
- Keep dev, CI, and (where possible) the deploy base aligned to the same image
  so the three don't diverge.
- Don't hardcode host paths or host-only assumptions; mount and configure
  through the devcontainer so the same setup works for anyone.

## When there is no dev container

- If the project would genuinely benefit (a non-trivial or shared toolchain) and
  has none, **offer to scaffold a minimal one** matching the stack — pin a base
  image and add only the features the stack needs (YAGNI, #4). Don't impose one
  on a throwaway script or a one-file task.
- Until one exists, say which host toolchain/versions you used, so results are
  reproducible.

## Don'ts

- Don't run dev/test/build on the host when a dev container exists "just this
  once" — that's the drift the container prevents.
- Don't commit personal IDE/host settings the container already standardizes
  (see `commits.md` — "What NOT to commit").
- Don't bloat the image with tools no task needs; keep it lean and current.
