# Contributing to Greenhouse

Thank you for helping the livestream examples grow! Community contributions are
welcome.

## Community expectations

Participation is governed by OllyGarden's
[Code of Conduct](https://github.com/ollygarden/.github/blob/main/CODE_OF_CONDUCT.md).
Report suspected vulnerabilities privately through the repository's
[security policy](https://github.com/ollygarden/greenhouse/security/policy), not
in a public issue. Project roles and decisions follow OllyGarden's
[governance policy](https://github.com/ollygarden/.github/blob/main/GOVERNANCE.md).

Contributions created with AI coding agents are welcome. A human contributor
must review and take responsibility for the result, disclose material agent
involvement in the pull request, and be able to respond to feedback.

## Getting started

1. Search existing issues and pull requests for related work. Open an issue
   before proposing a new session or substantially changing an old lesson.
2. Fork and clone the repository, then create a focused branch from `main`.
3. Read [AGENTS.md](AGENTS.md) and the README in the affected dated directory.
4. Keep the example self-contained and validate it with its documented
   toolchain.
5. Open a focused pull request with a summary, test plan, and the affected
   livestream session.

Use [Conventional Commits](https://www.conventionalcommits.org/), for example
`fix(otel-for-programmers): propagate request context`.

## Pull request expectations

- Keep changes focused on one session or one repository-level concern.
- Explain the teaching impact and any changed prerequisites or expected output.
- Update session and root documentation when commands, links, or structure move.
- Include exact validation commands and note anything that requires external
  services and could not be reproduced locally.
- Never commit secrets, customer data, production endpoints, or generated local
  environments.
- Resolve review threads and keep the branch current before requesting merge.

Maintainers review changes for correctness, clarity, safety, scope, and
reproducibility. Before a first pull request can be merged, contributors must
sign OllyGarden's
[Contributor License Agreement](https://github.com/ollygarden/.github/blob/main/CLA.md);
the CLA bot provides instructions on the pull request.
