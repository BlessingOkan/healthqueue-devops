# HealthQueue Appointment API - DORA Metrics Baseline
Synthetic dataset: 90 days, generated 2026-07-20

## Summary

| Metric | Value | Tier |
|---|---|---|
| Deployment Frequency | 3.73 / week (48 total) | High |
| Lead Time for Changes | 15.7 hours avg | High |
| Change Failure Rate | 12.5% | Elite |
| Mean Time to Restore | 4.16 hours avg | High |

## Analysis

The team deploys several times a week with same-day lead time -- solidly
High/High tier, short of Elite (multiple deploys/day, <1hr lead time).
Change failure rate and MTTR are the weaker pair and the more likely brake on
velocity right now.

## Toil Reduction Recommendations

1. Add a post-deploy smoke test gate to catch failures before they reach
   production, targeting the 12.5% change failure rate.
2. Add automatic rollback on failed health checks to cut MTTR from
   4.16 hours toward the Elite target of under 1 hour.
3. Encourage smaller, more frequent PRs to shrink both lead time and failure rate.
