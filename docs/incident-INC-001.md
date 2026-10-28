# Incident INC-001: Missing EC2 CPU Metrics

## 1. Incident Summary

- **Incident ID:** INC-001
- **Title:** Missing EC2 CPU Metrics
- **Service:** Amazon EC2 / Amazon CloudWatch
- **AWS Region:** us-east-1
- **Status:** Investigating
- **Severity:** Pending impact assessment
- **Incident Owner:** Not assigned in the available evidence
- **Start Time:** Not recorded
- **End Time:** Not recorded

## 2. Detection and Symptoms

The investigation identified the following symptoms:

- CloudWatch returned no CPUUtilization datapoints for the queried instance ID.
- A subsequent EC2 DescribeInstances request returned `InvalidInstanceID.NotFound`.

These observations establish a resource-identification or telemetry investigation need. They do not independently prove an EC2 outage, instance deletion, or customer impact.

## 3. Customer Impact

- **Confirmed impact:** Not established.
- **Service availability:** Not verified by the available evidence.
- **Affected customers:** Unknown.
- **Business impact:** Not assessed.

Do not report a customer-facing outage unless supported by service-health checks, application telemetry, customer reports, or other reliable evidence.

## 4. Investigation Timeline

| Sequence | Activity | Result |
|---|---|---|
| 1 | Queried CloudWatch CPUUtilization metrics | No datapoints returned |
| 2 | Queried EC2 using DescribeInstances | `InvalidInstanceID.NotFound` returned |
| 3 | Compared the resource identifier and region | The instance ID was not found by EC2 in the queried region |
| 4 | Determined customer impact and root cause | Still pending |

Exact timestamps were not provided. Record timestamps in UTC when verified; do not invent event times.

## 5. Evidence Collected

- **CloudWatch evidence:** Query returned no CPUUtilization datapoints.
- **EC2 evidence:** DescribeInstances returned `InvalidInstanceID.NotFound`.
- **Region checked:** us-east-1.
- **Resource ID:** Must be recorded from the original query or approved evidence.
- **Evidence references:** Attach approved logs, command output, or investigation links when available.

Avoid recording credentials, access keys, tokens, or other secrets in the incident report.

## 6. Investigation Steps

1. Confirm the instance ID against the approved resource inventory or deployment records.
2. Verify that the investigation is using the intended AWS account and region.
3. Check whether the resource exists and whether the identifier was copied correctly.
4. Review relevant CloudWatch metric dimensions, time range, and metric availability.
5. Check service health through approved application, load balancer, or infrastructure monitoring.
6. Record each check, its timestamp, the result, and the evidence reference.

Do not assume that missing metrics alone mean high CPU utilization or an application outage.

## 7. Root Cause

**Status:** Unknown.

The available evidence does not establish why CloudWatch returned no datapoints or why EC2 could not find the queried instance ID.

Update this section only when additional evidence supports a specific cause. If the cause cannot be established, document the remaining uncertainty during closure.

## 8. Immediate Response and Recovery

1. Preserve the original error messages and relevant timestamps.
2. Assess customer impact using reliable service-health evidence.
3. Reconcile the instance ID, AWS account, region, and approved inventory.
4. Restore or correct monitoring only after identifying the actual issue.
5. Do not launch replacement resources or make production changes without confirming the need and authorization.
6. Verify service health and telemetry after any approved remediation.

## 9. Recovery Criteria

The incident may be considered recovered when:

- The correct resource identity has been established, or the identifier discrepancy has been explained.
- Relevant service-health checks have been completed.
- Expected monitoring data is available again, where applicable.
- Any remediation has been verified.
- Remaining risks and unresolved questions have been documented.

## 10. Prevention and Follow-up

- Include AWS account, region, resource ID, and alarm name in alert context where appropriate.
- Alert on missing telemetry separately from threshold breaches such as high CPU.
- Maintain an approved resource inventory.
- Document the investigation commands and expected outcomes in the runbook.
- Review alert quality and add automated tests for missing or invalid incident fields.
- Assign follow-up actions to owners with target dates when the cause is established.

## 11. Closure

Keep the incident open while impact or recovery remains unverified.

Closure requires documented evidence of recovery or a justified decision that no remediation is needed. If the definitive root cause remains unknown, record the investigation performed, residual risk, and reason for closure.

- **Resolution:** Pending investigation.
- **Resolved At:** Not recorded.
- **Reviewed By:** Not assigned.
