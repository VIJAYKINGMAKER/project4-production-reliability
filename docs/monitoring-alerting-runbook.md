
# Monitoring and Alerting Runbook

## 1. Purpose

This runbook describes how to investigate AWS EC2 CPU alarms and missing CloudWatch metrics.

The objective is to distinguish:
- A genuine CPU utilization alarm.
- Missing or delayed metric data.
- An incorrect instance ID, AWS account, or region.
- A monitoring or configuration problem.
- A potential service impact that requires further investigation.

This runbook uses read-only AWS CLI commands. It does not create, restart, modify, or delete AWS resources.

## 2. Prerequisites

Before investigating, confirm:

- AWS CLI is installed and configured.
- The operator is authorized to read the relevant AWS resources and CloudWatch data.
- The correct AWS account and region are known.
- The incident or alert provides an instance ID, alarm name, and approximate event time.
- The investigation uses approved credentials and procedures.

Never place AWS access keys, passwords, or session tokens in the incident report.

## 3. Step 1 — Verify the AWS identity and region

First, identify the AWS account associated with the current CLI credentials:

```powershell
aws sts get-caller-identity
```

Why: This helps prevent investigating the wrong AWS account.

Set the intended region:

```powershell
$AWS_REGION = "us-east-1"
```

Use the region supplied by the alert or approved inventory. Do not assume every resource is in us-east-1.

## 4. Step 2 — Validate the EC2 resource

Set the instance ID from the original alert or approved inventory:

```powershell
$INSTANCE_ID = "i-REPLACE_WITH_REAL_INSTANCE_ID"
```

Replace the placeholder before executing the command.

Query EC2:

```powershell
aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $AWS_REGION
```

Interpret the result carefully:

- If the instance is returned, review its identity, state, and associated metadata.
- If `InvalidInstanceID.NotFound` is returned, verify the account, region, spelling of the ID, and approved inventory.
- If access is denied, investigate permissions through the approved access process.
- If the request times out or fails due to connectivity, investigate the CLI/network error separately.

A not-found response does not, by itself, prove that the instance was deleted.

## 5. Step 3 — Inspect the CloudWatch alarm

Set the alarm name from the alert:

```powershell
$ALARM_NAME = "REPLACE_WITH_REAL_ALARM_NAME"
```

Inspect the alarm:

```powershell
aws cloudwatch describe-alarms --alarm-names $ALARM_NAME --region $AWS_REGION
```

Review the returned alarm state, metric configuration, dimensions, threshold, evaluation periods, and reason for the state transition where available.

Do not infer an outage from the alarm state alone. Establish service impact using approved application and infrastructure health evidence.

## 6. Step 4 — Query CPUUtilization metrics

Set a UTC time window covering the incident:

```powershell
$START_TIME = "REPLACE_WITH_START_TIME_IN_UTC"
$END_TIME = "REPLACE_WITH_END_TIME_IN_UTC"
```

Replace both placeholders with valid UTC timestamps, for example `2026-10-28T08:00:00Z`. Use the actual incident window, not the example time.

Query the EC2 CPU metric:

```powershell
aws cloudwatch get-metric-statistics `
  --namespace AWS/EC2 `
  --metric-name CPUUtilization `
  --dimensions Name=InstanceId,Value=$INSTANCE_ID `
  --start-time $START_TIME `
  --end-time $END_TIME `
  --period 300 `
  --statistics Average `
  --region $AWS_REGION
```

This query requests five-minute CPU utilization averages for the specified instance and time window.

Interpretation:

- **Datapoints returned:** Review their timestamps and values against the alarm threshold.
- **No datapoints returned:** Check the time window, region, account, instance ID, metric dimensions, and whether the instance existed during that period.
- **Unexpected values:** Compare with the alarm configuration and other approved monitoring evidence.

Missing datapoints are not equivalent to zero CPU utilization.

## 7. Step 5 — Assess service impact

Check approved evidence such as:

- Application health endpoints and application logs.
- Load balancer target health, if applicable.
- Relevant service-level indicators and dashboards.
- Customer reports or support incidents.
- EC2 status checks and related infrastructure alarms.

Record what was checked, the time of the check, and the result.

If impact cannot be established, record it as unknown rather than claiming the service is healthy or unavailable.

## 8. Step 6 — Decision guide

| Observation | Next action |
|---|---|
| CPU datapoints exceed the configured threshold | Investigate workload behavior, service health, and the alarm evaluation window |
| Alarm is in ALARM but the current metric is normal | Review historical datapoints, evaluation periods, and state-transition timing |
| No CPU datapoints are returned | Validate the account, region, instance ID, time window, and metric dimensions |
| EC2 returns InvalidInstanceID.NotFound | Reconcile the resource ID and AWS account/region against approved inventory |
| AWS CLI returns AccessDenied | Follow the approved permissions and escalation process |
| Service impact is suspected | Escalate according to the incident severity and response policy |
| Evidence remains inconclusive | Preserve evidence, document uncertainty, and keep the incident open as appropriate |

## 9. Evidence to Record

For each investigation, record:

- Incident ID and alarm name.
- AWS account identifier and region.
- Instance ID, where applicable.
- Incident time window in UTC.
- Exact error messages and relevant command results.
- CloudWatch datapoint timestamps and values, if returned.
- Service-health checks performed and their results.
- Customer impact: confirmed, not observed in the checks performed, or unknown.
- Investigation owner and escalation details.
- Remediation performed, authorization, and verification results.

Store evidence in approved locations and do not include secrets.

## 10. Recovery and Closure

Before declaring recovery:

1. Establish the correct resource identity or document the discrepancy.
2. Complete relevant service-health checks.
3. Confirm expected monitoring data is available when applicable.
4. Verify any approved remediation.
5. Record residual risks and unresolved questions.
6. Follow the organization's incident review and closure process.

A definitive root cause is desirable but must not be invented. If it remains unknown, document the evidence, investigation performed, remaining uncertainty, and rationale for closure.

## 11. Safety Rules

- Use the intended AWS account and region.
- Use read-only commands during initial triage.
- Do not restart, replace, or delete infrastructure solely because metrics are missing.
- Do not treat missing telemetry as proof of an outage or zero utilization.
- Follow approved authorization and escalation procedures before production changes.
