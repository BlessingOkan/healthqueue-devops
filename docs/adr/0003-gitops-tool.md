# ADR 0003: GitOps Deployment Tool

## Status
Accepted

## Context
The team needs the Kubernetes cluster to stay in sync with what's declared
in Git, without engineers running manual `kubectl apply` commands.

## Decision
Use Argo CD for GitOps reconciliation.

## Consequences
- Argo CD continuously watches the Git repo and reconciles cluster state
  to match -- including self-healing if someone manually changes something
  in the cluster directly, it gets reverted back to match Git
- All deploys become PR-driven: a change to the manifests directory in Git
  is the only way to change what's running, giving a clear audit trail
- Trade-off vs Flux (the other common GitOps tool): Argo CD has a more
  approachable web UI, which matters for a team still building GitOps
  familiarity, at the cost of a slightly heavier footprint to run
