# Repository guidance

## Purpose

Greenhouse is OllyGarden's public collection of code, examples, and resources
grown during livestream sessions. Each dated directory captures a specific
session and should remain understandable and runnable on its own.

## Repository model

- Top-level directories use the session date and topic, for example
  `2026-01-21-tulip-downstream-distributions/`.
- Each session owns its source, configuration, dependencies, and detailed
  README. Do not create hidden coupling between dated examples.
- The root [README.md](README.md) is the session index and should link to the
  correct directory and recording.
- `.github/workflows/` contains validation scoped to particular examples. Read
  path filters and external-system effects before changing those paths.

## Working in this repository

Start with the README inside the affected session and use its documented
toolchain. Validation is example-specific:

- Go examples: run `go test ./...` and `go vet ./...` from the directory that
  contains `go.mod`; run the documented service or build command when practical.
- Python examples: use a virtual environment, install the session's pinned
  requirements, and run at least `python -m compileall .`; exercise both manual
  and auto-instrumented paths when their behavior changes.
- Collector distribution examples: run the local `make build` and
  `make validate` targets when changing a manifest or configuration. Docker and
  dependency downloads may be required.
- Helm examples: run `helm lint` and `helm template` with the relevant values.
  Do not apply examples to a Kubernetes cluster as routine PR validation.
- Root-only documentation changes: verify links, Markdown structure, and that
  the session index matches the dated directories.

## Example guardrails

- Preserve the educational intent and historical context of a session. Prefer a
  focused correction with a note over silently rewriting an old example into a
  different architecture.
- Keep each example self-contained. If multiple sessions need the same helper,
  duplicate the small teaching artifact or document an explicit dependency
  rather than making one dated directory import another.
- Examples may simplify production concerns for teaching, but state those
  simplifications clearly. Do not describe demo storage, authentication, TLS,
  resource limits, or in-memory state as production-ready.
- Never commit API keys, `.env` files, cloud credentials, kubeconfigs, customer
  telemetry, or production endpoints. Keep `.env.example` values synthetic.
- Use current OpenTelemetry APIs and semantic conventions for new sessions.
  When repairing an older session, preserve its lesson while documenting any
  version or compatibility requirement.
- Update a session README when commands, prerequisites, ports, component
  versions, configuration, or expected output changes.
- Keep the root index chronological data and links accurate. A new session needs
  a dated directory, a useful README, and an entry in the root session table.
- Inspect workflow path filters before moving or renaming examples. Some paths
  trigger Collector builds or external changelog analysis; do not broaden
  cluster or cloud access as part of unrelated work.

## Pull requests

Follow [CONTRIBUTING.md](CONTRIBUTING.md). Name the affected livestream session,
explain the teaching impact, and include the exact example-specific validation
performed.
