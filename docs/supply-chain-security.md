# Supply Chain Security Summary - Appointment API Pipeline

## Overview
The CI/CD pipeline (`.github/workflows/ci-cd.yml`) implements supply chain
security controls at each stage: build, scan, sign, and attest. This
document maps those controls to the SLSA (Supply-chain Levels for Software
Artifacts) framework.

## Controls in the Pipeline

**1. Vulnerability Scanning (Trivy)**
Every image build is scanned for CRITICAL/HIGH vulnerabilities before
publishing. Results upload to GitHub's Security tab for tracking over time.

**2. SBOM Generation (Syft)**
A Software Bill of Materials in SPDX JSON format is generated for every
image, listing every dependency and package version included in the build.
This lets the team (or an auditor) answer "are we affected by CVE-X" in
minutes instead of days.

**3. Artifact Signing (Cosign, keyless)**
Every image is cryptographically signed using Sigstore's keyless signing
via GitHub's OIDC identity -- no private signing keys to manage, rotate, or
leak. Signatures prove the image came from this exact pipeline run and
hasn't been tampered with since.

**4. SBOM Attestation**
The SBOM itself is attached to the image as a signed attestation, not just
generated as a loose file -- tying dependency data cryptographically to the
specific image digest it describes.

**5. Build Provenance (SLSA)**
GitHub's official provenance generator (`actions/attest-build-provenance`)
records exactly which workflow, commit, and repository produced the image,
signed and verifiable.

## SLSA Level Mapping

| SLSA Requirement | Status | How |
|---|---|---|
| Scripted build | Met | GitHub Actions workflow, not manual steps |
| Provenance generated | Met | `attest-build-provenance` action |
| Provenance signed | Met | Signed via GitHub OIDC/Sigstore |
| Build service isolation | Met | GitHub-hosted runners, ephemeral per run |
| Source verified | Partial | Checkout via `actions/checkout`, no branch protection rules configured yet |

This pipeline currently sits at **SLSA Level 2**: builds are scripted,
provenance is generated and signed, and the build runs on isolated,
ephemeral infrastructure. Reaching Level 3 would require adding branch
protection rules (required reviews, no force-push to main) and hardening
the build service further against tampering mid-build -- a natural next
step, not yet implemented here.

## Trade-offs
Keyless signing (via GitHub OIDC) was chosen over managing a long-lived
signing key: it removes an entire class of key-leakage risk at the cost of
being tied to GitHub's identity provider. If the team ever moves off
GitHub Actions, signing would need to be reconfigured.
