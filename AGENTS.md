# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **Cursor AI agent skills repository** for the [Customer.io CLI](https://github.com/customerio/cli) (`cio`). It contains skill definitions (markdown files under `.agents/skills/cio/`) and a `skills-lock.json` lockfile. There is no application code, build system, or test suite.

### Key service

| Service | How to verify |
|---|---|
| `cio` CLI (v0.0.5+) | `cio --version` / `cio prime` |

### Running the CLI

- **Install**: `npm i -g @customerio/cli`
- **Prime** (dumps full LLM-ready reference): `cio prime`
- **Auth**: `cio auth login` (opens browser flow for `sa_live_` token) or `echo "$CIO_TOKEN" | cio auth login --with-token`
- **Auth check**: `cio auth status`

### Authentication

The CLI requires a Customer.io service account token (`sa_live_...`). If the `CIO_TOKEN` environment variable is set, the CLI uses it automatically. Otherwise, run `cio auth login` to authenticate interactively.

To authenticate non-interactively (e.g., in CI or automated flows):
```bash
echo "$CIO_TOKEN" | cio auth login --with-token
```

### Skill files

The skill definitions on the feature branch live at `.agents/skills/cio/`:
- `SKILL.md` — main entry point; describes when to invoke the CLI
- `onboarding.md` — guides users through signup, domain setup, first email
- `billing.md` — handles plans, pricing, go-live questions
- `integration.md` — SDK install, identify/track, transactional sends

### Lint / Test / Build

There are no lint, test, or build steps for this repository. Validation is limited to verifying the CLI installs and runs correctly (`cio --version`, `cio prime`).
