#!/usr/bin/env python3
"""
Generates synthetic 90-day deployment data for HealthQueue's appointment-api
and computes DORA metrics against Elite/High/Medium/Low benchmarks.
"""

import csv
import random
import statistics
from datetime import datetime, timedelta

random.seed(42)

NUM_DAYS = 90
START_DATE = datetime(2026, 4, 20)
DEPLOY_PROB_WEEKDAY = 0.65
DEPLOY_PROB_WEEKEND = 0.05
FAILURE_RATE = 0.12
LEAD_TIME_MEAN_HOURS = 14
LEAD_TIME_STDDEV_HOURS = 6
MTTR_MEAN_HOURS = 3.5
MTTR_STDDEV_HOURS = 2


def generate_deployments():
    deployments = []
    current = START_DATE
    for _ in range(NUM_DAYS):
        is_weekend = current.weekday() >= 5
        prob = DEPLOY_PROB_WEEKEND if is_weekend else DEPLOY_PROB_WEEKDAY
        if random.random() < prob:
            lead_time = max(0.5, random.gauss(LEAD_TIME_MEAN_HOURS, LEAD_TIME_STDDEV_HOURS))
            failed = random.random() < FAILURE_RATE
            restore_time = max(0.25, random.gauss(MTTR_MEAN_HOURS, MTTR_STDDEV_HOURS)) if failed else None
            deployments.append({
                "date": current.strftime("%Y-%m-%d"),
                "lead_time_hours": round(lead_time, 2),
                "failed": failed,
                "restore_time_hours": round(restore_time, 2) if restore_time else "",
            })
        current += timedelta(days=1)
    return deployments


def compute_metrics(deployments):
    num_deploys = len(deployments)
    num_failures = sum(1 for d in deployments if d["failed"])
    deploys_per_week = num_deploys / (NUM_DAYS / 7)
    lead_times = [d["lead_time_hours"] for d in deployments]
    avg_lead_time = statistics.mean(lead_times) if lead_times else 0
    cfr = (num_failures / num_deploys * 100) if num_deploys else 0
    restore_times = [d["restore_time_hours"] for d in deployments if d["restore_time_hours"] != ""]
    avg_mttr = statistics.mean(restore_times) if restore_times else 0
    return {
        "total_deployments": num_deploys,
        "deploys_per_week": round(deploys_per_week, 2),
        "avg_lead_time_hours": round(avg_lead_time, 2),
        "change_failure_rate_pct": round(cfr, 2),
        "avg_mttr_hours": round(avg_mttr, 2),
        "num_failures": num_failures,
    }


def write_csv(deployments, path="dora_deployments.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "lead_time_hours", "failed", "restore_time_hours"])
        writer.writeheader()
        writer.writerows(deployments)


def write_report(metrics, path="dora_report.md"):
    freq_tier = "Elite" if metrics["deploys_per_week"] >= 7 else "High" if metrics["deploys_per_week"] >= 0.25 else "Medium"
    lead_tier = "Elite" if metrics["avg_lead_time_hours"] < 1 else "High" if metrics["avg_lead_time_hours"] <= 168 else "Medium"
    cfr_tier = "Elite" if metrics["change_failure_rate_pct"] <= 15 else "High/Medium" if metrics["change_failure_rate_pct"] <= 30 else "Low"
    mttr_tier = "Elite" if metrics["avg_mttr_hours"] < 1 else "High" if metrics["avg_mttr_hours"] <= 24 else "Medium"

    report = f"""# HealthQueue Appointment API - DORA Metrics Baseline
Synthetic dataset: {NUM_DAYS} days, generated {datetime.now().strftime("%Y-%m-%d")}

## Summary

| Metric | Value | Tier |
|---|---|---|
| Deployment Frequency | {metrics['deploys_per_week']} / week ({metrics['total_deployments']} total) | {freq_tier} |
| Lead Time for Changes | {metrics['avg_lead_time_hours']} hours avg | {lead_tier} |
| Change Failure Rate | {metrics['change_failure_rate_pct']}% | {cfr_tier} |
| Mean Time to Restore | {metrics['avg_mttr_hours']} hours avg | {mttr_tier} |

## Analysis

The team deploys several times a week with same-day lead time -- solidly
{freq_tier}/{lead_tier} tier, short of Elite (multiple deploys/day, <1hr lead time).
Change failure rate and MTTR are the weaker pair and the more likely brake on
velocity right now.

## Toil Reduction Recommendations

1. Add a post-deploy smoke test gate to catch failures before they reach
   production, targeting the {metrics['change_failure_rate_pct']}% change failure rate.
2. Add automatic rollback on failed health checks to cut MTTR from
   {metrics['avg_mttr_hours']} hours toward the Elite target of under 1 hour.
3. Encourage smaller, more frequent PRs to shrink both lead time and failure rate.
"""
    with open(path, "w") as f:
        f.write(report)


if __name__ == "__main__":
    deployments = generate_deployments()
    metrics = compute_metrics(deployments)
    write_csv(deployments)
    write_report(metrics)
    print(f"Generated {len(deployments)} deployments over {NUM_DAYS} days.")
    print(f"Deploy freq: {metrics['deploys_per_week']}/week | Lead time: {metrics['avg_lead_time_hours']}h | CFR: {metrics['change_failure_rate_pct']}% | MTTR: {metrics['avg_mttr_hours']}h")
