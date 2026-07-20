# Observability Plan - Appointment Scheduling API

## 1. Service Overview
The appointment-api lets patients view provider availability and book,
reschedule, or cancel appointments. What matters most: is it up, and is it
fast enough to use during a phone call or in-office check-in.

## 2. SLIs (Service Level Indicators)

| SLI | Definition | Measurement |
|---|---|---|
| Availability | % of requests returning non-5xx | `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` |
| Latency | % of requests under 200ms | `histogram_quantile(0.95, http_request_duration_seconds_bucket)` |
| Booking Success Rate | % of booking requests that succeed | `sum(rate(booking_requests_total{status="success"}[5m])) / sum(rate(booking_requests_total[5m]))` |

## 3. SLOs (Service Level Objectives)

| SLI | Target | Window |
|---|---|---|
| Availability | 99.9% | Rolling 30 days |
| Latency (p95) | < 200ms | Rolling 30 days |
| Booking Success Rate | 99.5% | Rolling 30 days |

99.9% ("three nines") was chosen over 99.99% because this is a scheduling
API, not a life-critical system -- a few minutes of downtime is an
inconvenience, not an emergency, and 99.99% would require infrastructure
this team doesn't need yet.

## 4. Error Budget

For 99.9% availability over 30 days:
