# Runbook - Appointment API

## Common Operations

**Check pipeline status:** GitHub repo -> Actions tab

**Deploy a change:** Push to main. The pipeline builds, scans, signs, and
publishes the image, then updates the GitOps manifest, which Argo CD picks
up automatically.

**Roll back a bad deploy:** Revert the image-tag commit in the manifests
directory and push. Argo CD reconciles the cluster back to the previous
image within seconds.

**Check current SLO status:** See the error budget calculation in
`docs/observability-plan.md`. Grafana dashboard (once deployed) shows live
burn-down.

## Incident Response

1. Check Argo CD sync status first -- is the cluster actually running what
   Git says it should be?
2. Check the Vulnerability Scan / Build job logs in GitHub Actions if a
   recent deploy is suspected.
3. If rollback is needed, see "Roll back a bad deploy" above.
4. Log the incident's impact on the error budget (see observability plan).

## Local Development

See README.md for running the app, tests, and infrastructure locally.
