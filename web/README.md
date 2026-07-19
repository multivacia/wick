# WICK web — UX foundation scaffold (I1)

Demonstration scaffold only. **No operational screens implemented.**

This package is the frontend toolchain foundation for future WICK UX work.
It must not display readiness, collection status, host/scheduler state,
profit, return, accuracy, edge, or validation results.

## Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 22 LTS (see `.nvmrc`) |
| pnpm | 10.33.3 (`packageManager` field) |

### Windows

1. Install Node.js 22 LTS from https://nodejs.org or `winget install OpenJS.NodeJS.LTS`
2. Enable Corepack and activate pnpm:

```powershell
corepack enable
corepack prepare pnpm@10.33.3 --activate
node -v
pnpm -v
```

### Linux

```bash
# nvm example
nvm install 22
nvm use
corepack enable
corepack prepare pnpm@10.33.3 --activate
node -v
pnpm -v
```

Docker is **not** required for frontend development.

## Commands

Run from the repository root:

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web dev
pnpm --dir web typecheck
pnpm --dir web lint
pnpm --dir web test
pnpm --dir web test:a11y
pnpm --dir web build
pnpm --dir web audit
pnpm --dir web licenses
```

Or from `web/`:

```bash
pnpm install --frozen-lockfile
pnpm dev
pnpm typecheck
pnpm lint
pnpm test
pnpm test:a11y
pnpm build
pnpm audit
pnpm licenses
```

## Environment variables (`VITE_` rule)

Vite only exposes environment variables prefixed with `VITE_` to client code.
Those values are embedded in the production bundle.

- Allowed: non-secret public flags such as `VITE_APP_TITLE`
- Forbidden in `VITE_*`: secrets, `DATABASE_URL`, provider tokens, host credentials, private endpoints

Do not commit `.env` files with secrets. Prefer local unsynced `.env.local` for experiments.

## Source maps

Production builds disable client source maps (`build.sourcemap = false`) to avoid leaking
implementation detail through public artifacts.

## Dependency governance

- Lockfile (`pnpm-lock.yaml`) is required and authoritative
- Exact versions are pinned in `package.json` (no floating ranges)
- `ignore-scripts=true` in `.npmrc` blocks unapproved postinstall scripts
- `pnpm audit` runs in CI for production dependency advisories
- `pnpm licenses` lists production licenses (allowlist: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC; others need human exception)
- New runtime dependencies require human approval (owner: Gustavo Almeida)
- Radix and other UI libraries are **not** installed in I1

## Accessibility

Target: WCAG 2.2 AA (policy). I1 provides an axe-core smoke harness only.
Component-level a11y gates start at later increments.

## Out of scope (I1)

- Design tokens / themes
- Design-system components
- Router / app shell / MVP screens
- API clients / operational data
- Radix UI
- Charts, auth, analytics, remote fonts
