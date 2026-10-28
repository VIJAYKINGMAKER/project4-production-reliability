
from datetime import datetime, timezone
import hashlib
import json


def handler(event, context=None):
    """Build an incident record from an alert payload; makes no AWS API calls."""
    required = ("alarm_name", "state", "region")
    missing = [key for key in required if not event.get(key)]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))

    state = str(event["state"]).upper()

    if state not in ("ALARM", "OK"):
        raise ValueError(f"Unsupported alarm state: {state}")

    severity = "P2" if state == "ALARM" else "P3"
    resource_id = event.get("resource_id", "unknown")

    # Stable across repeated deliveries of the same alarm/resource.
    identity = {
        "alarm_name": event["alarm_name"],
        "region": event["region"],
        "resource_id": resource_id,
    }
    identity_json = json.dumps(identity, sort_keys=True)
    deduplication_key = hashlib.sha256(
        identity_json.encode("utf-8")
    ).hexdigest()

    return {
        "incident_id": event.get("incident_id", "AUTO-INCIDENT"),
        "deduplication_key": deduplication_key,
        "alarm_name": event["alarm_name"],
        "state": state,
        "severity": severity,
        "region": event["region"],
        "resource_id": resource_id,
        "summary": event.get("summary", "Monitoring alert received"),
        "customer_impact": "Not yet assessed",
        "recommended_action": (
            "Assess service impact and investigate using approved evidence."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
