"""AWS Lambda entry point for production incident automation."""

from src.event_adapter import adapt_eventbridge_event
from src.incident_handler import handler as create_incident


def lambda_handler(event, context):
    """Convert an EventBridge alarm event into an incident record."""
    incident_payload = adapt_eventbridge_event(event)
    return create_incident(incident_payload, context)
