
"""Translate EventBridge alarm state-change events into incident payloads."""


def adapt_eventbridge_event(event):
    """Convert an EventBridge CloudWatch alarm event to our internal format."""
    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary.")

    detail = event.get("detail")
    if not isinstance(detail, dict):
        raise ValueError("Event must contain a detail dictionary.")

    alarm_name = event.get("resources")
    if not isinstance(alarm_name, list) or not alarm_name:
        raise ValueError("Event must contain a non-empty resources list.")

    alarm_arn = alarm_name[0]
    if not isinstance(alarm_arn, str) or not alarm_arn.strip():
        raise ValueError("The first resource must be a non-empty alarm ARN.")

    state_info = detail.get("state")
    if not isinstance(state_info, dict):
        raise ValueError("Event detail must contain a state dictionary.")

    state = state_info.get("value")
    if not isinstance(state, str) or state.strip().upper() not in ("ALARM", "OK"):
        raise ValueError("Event state must be ALARM or OK.")

    region = event.get("region")
    if not isinstance(region, str) or not region.strip():
        raise ValueError("Event must contain a non-empty region.")

    # EventBridge alarm resource ARNs have this structure:
    # arn:aws:cloudwatch:region:account-id:alarm:alarm-name
    arn_parts = alarm_arn.split(":")
    if len(arn_parts) < 7 or arn_parts[2] != "cloudwatch" or arn_parts[5] != "alarm":
        raise ValueError("Event resource must be a CloudWatch alarm ARN.")

    arn_region = arn_parts[3]
    if arn_region != region.strip():
        raise ValueError("Event region does not match the alarm ARN region.")

    normalized_state = state.strip().upper()
    reason = state_info.get("reason", "CloudWatch alarm state changed")
    if not isinstance(reason, str) or not reason.strip():
        reason = "CloudWatch alarm state changed"

    return {
        "alarm_name": ":".join(arn_parts[6:]),
        "state": normalized_state,
        "region": region.strip(),
        # CloudWatch alarm events do not always identify one EC2 resource.
        "resource_id": "unknown",
        "summary": reason.strip(),
    }
