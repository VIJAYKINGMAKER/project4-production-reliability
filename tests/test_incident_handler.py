
import unittest
from src.incident_handler import handler


class IncidentHandlerTests(unittest.TestCase):
    def test_alarm_creates_p2_incident(self):
        result = handler({
            "alarm_name": "HighCPU",
            "state": "ALARM",
            "region": "us-east-1",
            "resource_id": "i-example",
        })
        self.assertEqual(result["severity"], "P2")
        self.assertEqual(result["state"], "ALARM")
        self.assertEqual(result["resource_id"], "i-example")
        self.assertEqual(result["customer_impact"], "Not yet assessed")
        self.assertTrue(result["deduplication_key"])

    def test_ok_state_creates_p3_record(self):
        result = handler({
            "alarm_name": "HighCPU",
            "state": "OK",
            "region": "us-east-1",
        })
        self.assertEqual(result["severity"], "P3")

    def test_missing_required_field_fails(self):
        with self.assertRaises(ValueError):
            handler({"alarm_name": "HighCPU", "state": "ALARM"})

    def test_unsupported_state_fails(self):
        with self.assertRaisesRegex(ValueError, "Unsupported alarm state"):
            handler({
                "alarm_name": "HighCPU",
                "state": "UNKNOWN",
                "region": "us-east-1",
            })

    def test_same_alarm_and_resource_produce_same_key(self):
        event = {
            "alarm_name": "HighCPU",
            "state": "ALARM",
            "region": "us-east-1",
            "resource_id": "i-example",
        }
        first = handler(event)
        second = handler(event)

        self.assertEqual(
            first["deduplication_key"],
            second["deduplication_key"],
        )
        self.assertNotEqual(first["created_at"], second["created_at"])

    def test_different_resources_produce_different_keys(self):
        base_event = {
            "alarm_name": "HighCPU",
            "state": "ALARM",
            "region": "us-east-1",
            "resource_id": "i-example-1",
        }
        other_event = {
            **base_event,
            "resource_id": "i-example-2",
        }

        self.assertNotEqual(
            handler(base_event)["deduplication_key"],
            handler(other_event)["deduplication_key"],
        )


if __name__ == "__main__":
    unittest.main()
