
from datetime import datetime, timezone
import hashlib
import json


def handler(event, context=None):
    """Build an incident record from an alert payload; makes no AWS API calls."""
    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary.")

    required = ("alarm_name", "state", "region")
    missing = [
        key
        for key in required
        if key not in event
        or not isinstance(event[key], str)
        or not event[key].strip()
    ]

    if missing:
        raise ValueError(
            "Missing or invalid required fields: " + ", ".join(missing)
        )

    alarm_name = event["alarm_name"].strip()
    state = event["state"].strip().upper()
    region = event["region"].strip()

    if state not in ("ALARM", "OK"):
        raise ValueError(f"Unsupported alarm state: {state}")

    resource_id = event.get("resource_id", "unknown")
    if not isinstance(resource_id, str) or not resource_id.strip():
        raise ValueError("resource_id must be a non-empty string.")

    resource_id = resource_id.strip()

    incident_id = event.get("incident_id", "AUTO-INCIDENT")
    if not isinstance(incident_id, str) or not incident_id.strip():
        raise ValueError("incident_id must be a non-empty string.")

    summary = event.get("summary", "Monitoring alert received")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("summary must be a non-empty string.")

    severity = "P2" if state == "ALARM" else "P3"

    # Stable across repeated deliveries of the same alarm/resource.
    identity = {
        "alarm_name": alarm_name,
        "region": region,
        "resource_id": resource_id,
    }
    identity_json = json.dumps(identity, sort_keys=True)
    deduplication_key = hashlib.sha256(
        identity_json.encode("utf-8")
    ).hexdigest()

    return {
        "incident_id": incident_id.strip(),
        "deduplication_key": deduplication_key,
        "alarm_name": alarm_name,
        "state": state,
        "severity": severity,
        "region": region,
        "resource_id": resource_id,
        "summary": summary.strip(),
        "customer_impact": "Not yet assessed",
        "recommended_action": (
            "Assess service impact and investigate using approved evidence."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
