# HealthQueue Appointment API - DevOps Reference Pipeline

A production-grade DevOps pipeline for HealthQueue's patient-facing appointment scheduling API, built as the team's reference architecture.

## What's in this repo

- `app.py`, `Dockerfile`, `requirements.txt`, `test_app.py` -- the Flask appointment API and its test suite
- `.github/workflows/ci-cd.yml` -- CI/CD pipeline: build, test, vulnerability scan, SBOM generation, artifact signing, SLSA provenance
- `infra/` -- OpenTofu configuration provisioning an S3 bucket (build artifacts) and an IAM role (CI pipeline permissions), with local state
- `scripts/generate_dora_metrics.py` -- generates 90 days of synthetic deployment data and analyzes it against DORA benchmarks
- `docs/observability-plan.md` -- SLIs, SLOs, and error budget for the API
- `docs/supply-chain-security.md` -- SLSA level mapping and pipeline security controls
- `docs/adr/` -- Architecture Decision Records
- `docs/runbook.md` -- day-2 operations guide

## Running it locally

App:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 app.py

Tests:

    pytest

Infrastructure (against LocalStack, no AWS account needed):

    localstack start -d
    cd infra
    tofu init
    tofu apply

DORA metrics:

    cd scripts
    python3 generate_dora_metrics.py

## CI/CD Pipeline

Every push to main runs three jobs in sequence: Build & Test, Vulnerability Scan (Trivy), and Build/Sign/SBOM/Publish. See docs/supply-chain-security.md for how this maps to SLSA levels.

## Kubernetes / GitOps

The containerized app deploys to Kubernetes via Argo CD, reconciling from the manifests/ directory whenever it changes in Git.
