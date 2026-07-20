# ADR 0002: Infrastructure as Code Tool

## Status
Accepted

## Context
The team needs to provision and track cloud infrastructure (S3, IAM) with
version-controlled state, without vendor lock-in to a single IaC tool.

## Decision
Use OpenTofu (the open-source Terraform fork) instead of proprietary
Terraform, with a local state backend for now.

## Consequences
- OpenTofu's syntax and provider ecosystem are identical to Terraform, so
  the team's existing HCL knowledge transfers directly
- Local state backend was chosen over S3 remote state because standing up
  a remote backend requires an already-provisioned S3 bucket + DynamoDB
  lock table -- a bootstrapping problem. This is a known trade-off:
  local state doesn't support team-wide locking or shared visibility.
  Moving to an S3 backend is the natural next step once the team has a
  provisioned AWS account.
- Resources were validated and applied against LocalStack (a local AWS
  simulator) rather than a real AWS account, to avoid requiring billing
  setup for this reference architecture. The same config works unchanged
  against real AWS by removing the LocalStack endpoint overrides.
