
import unittest

from src.event_adapter import adapt_eventbridge_event
from src.incident_handler import handler


def make_event(state="ALARM"):
    return {
        "source": "aws.cloudwatch",
        "detail-type": "CloudWatch Alarm State Change",
        "region": "us-east-1",
        "resources": [
            "arn:aws:cloudwatch:us-east-1:123456789012:alarm:HighCPU"
        ],
        "detail": {
            "state": {
                "value": state,
                "reason": "Alarm threshold crossed",
            }
        },
    }


class EventAdapterTests(unittest.TestCase):
    def test_alarm_event_is_converted(self):
        result = adapt_eventbridge_event(make_event())

        self.assertEqual(result["alarm_name"], "HighCPU")
        self.assertEqual(result["state"], "ALARM")
        self.assertEqual(result["region"], "us-east-1")
        self.assertEqual(result["resource_id"], "unknown")
        self.assertEqual(result["summary"], "Alarm threshold crossed")

    def test_ok_event_is_converted(self):
        result = adapt_eventbridge_event(make_event("OK"))
        self.assertEqual(result["state"], "OK")

    def test_non_dictionary_event_fails(self):
        with self.assertRaisesRegex(ValueError, "dictionary"):
            adapt_eventbridge_event(None)

    def test_missing_detail_fails(self):
        with self.assertRaisesRegex(ValueError, "detail dictionary"):
            adapt_eventbridge_event({})

    def test_missing_resources_fails(self):
        event = make_event()
        event["resources"] = []

        with self.assertRaisesRegex(ValueError, "resources list"):
            adapt_eventbridge_event(event)

    def test_invalid_alarm_arn_fails(self):
        event = make_event()
        event["resources"] = ["not-an-arn"]

        with self.assertRaisesRegex(ValueError, "CloudWatch alarm ARN"):
            adapt_eventbridge_event(event)

    def test_region_mismatch_fails(self):
        event = make_event()
        event["region"] = "eu-west-1"

        with self.assertRaisesRegex(ValueError, "region does not match"):
            adapt_eventbridge_event(event)

    def test_unsupported_state_fails(self):
        with self.assertRaisesRegex(ValueError, "ALARM or OK"):
            adapt_eventbridge_event(make_event("INSUFFICIENT_DATA"))

    def test_alarm_event_creates_incident_end_to_end(self):
        # Step 1: Simulate a CloudWatch alarm event from EventBridge.
        event = make_event("ALARM")

        # Step 2: Convert the AWS event to our internal payload format.
        incident_payload = adapt_eventbridge_event(event)

        # Step 3: Pass the payload to the incident handler.
        incident = handler(incident_payload)

        # Step 4: Verify the generated incident record.
        self.assertEqual(incident["alarm_name"], "HighCPU")
        self.assertEqual(incident["state"], "ALARM")
        self.assertEqual(incident["severity"], "P2")
        self.assertEqual(incident["region"], "us-east-1")
        self.assertEqual(incident["summary"], "Alarm threshold crossed")
        self.assertTrue(incident["deduplication_key"])
        self.assertEqual(incident["resource_id"], "unknown")


if __name__ == "__main__":
    unittest.main()
