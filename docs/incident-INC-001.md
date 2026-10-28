# Incident INC-001: Missing EC2 CPU Metrics

## Status
Investigating  root cause not established.

## Environment
AWS region: us-east-1
Service: Amazon EC2 / Amazon CloudWatch

## Symptoms
- CloudWatch returned no CPUUtilization datapoints for the queried instance ID.
- The subsequent EC2 DescribeInstances request returned InvalidInstanceID.NotFound.

## Impact
Customer impact has not been established. No claim of service outage is made.

## Investigation
- Reviewed CloudWatch metric discovery and CPU datapoint results.
- Compared the instance ID with the EC2 API response.
- The ID was not found by EC2 in the queried region.

## Root Cause
Unknown. The available evidence does not establish why the discrepancy occurred.

## Immediate Response
1. Record the error and investigation timeline.
2. Assess whether a customer-facing service is affected.
3. Reconcile the resource identifier, region and approved inventory.
4. Do not launch replacement resources without confirming need and authorization.

## Recovery Criteria
Confirm the correct resource identity, establish service health using reliable evidence,
and verify monitoring data is available when applicable.

## Prevention
- Include region and resource identifiers in alerts.
- Alert on missing telemetry separately from high CPU utilization.
- Maintain an approved resource inventory and an incident runbook.

## Closure
Keep open until impact and cause are understood, or document why the incident can
be closed without determining a definitive root cause.
