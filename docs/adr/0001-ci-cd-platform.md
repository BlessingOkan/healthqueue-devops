# ADR 0001: CI/CD Platform Choice

## Status
Accepted

## Context
The team needs a CI/CD platform that supports automated build, test,
vulnerability scanning, SBOM generation, and artifact signing, without
adding a separate hosted CI vendor to manage.

## Decision
Use GitHub Actions, since the code already lives on GitHub.

## Consequences
- No separate CI vendor account, billing, or auth to manage
- Native integration with GitHub's Security tab (SARIF upload) and OIDC
  identity (used for keyless artifact signing)
- Trade-off: tighter coupling to GitHub specifically; migrating CI
  elsewhere later would mean rewriting the workflow syntax
