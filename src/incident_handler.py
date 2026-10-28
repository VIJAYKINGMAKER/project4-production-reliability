from datetime import datetime, timezone


def handler(event, context=None):
    """Build an incident record from an alert payload; makes no AWS API calls."""
    required = ("alarm_name", "state", "region")
    missing = [key for key in required if not event.get(key)]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))

    state = str(event["state"]).upper()
    severity = "P2" if state == "ALARM" else "P3"

    return {
        "incident_id": event.get("incident_id", "AUTO-INCIDENT"),
        "alarm_name": event["alarm_name"],
        "state": state,
        "severity": severity,
        "region": event["region"],
        "resource_id": event.get("resource_id", "unknown"),
        "summary": event.get("summary", "Monitoring alert received"),
        "customer_impact": "Not yet assessed",
        "recommended_action": (
            "Assess service impact and investigate using approved evidence."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
