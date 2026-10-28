
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

    def test_none_event_fails_with_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Event must be a dictionary"):
            handler(None)

    def test_non_dictionary_event_fails(self):
        for event in ([], "invalid", 123):
            with self.subTest(event=event):
                with self.assertRaisesRegex(
                    ValueError, "Event must be a dictionary"
                ):
                    handler(event)

    def test_whitespace_only_required_field_fails(self):
        for field in ("alarm_name", "state", "region"):
            event = {
                "alarm_name": "HighCPU",
                "state": "ALARM",
                "region": "us-east-1",
            }
            event[field] = "   "

            with self.subTest(field=field):
                with self.assertRaisesRegex(
                    ValueError, "Missing or invalid required fields"
                ):
                    handler(event)

    def test_required_field_with_wrong_type_fails(self):
        event = {
            "alarm_name": "HighCPU",
            "state": "ALARM",
            "region": "us-east-1",
        }
        event["alarm_name"] = 123

        with self.assertRaisesRegex(
            ValueError, "Missing or invalid required fields"
        ):
            handler(event)

    def test_state_is_trimmed_and_normalized(self):
        result = handler({
            "alarm_name": " HighCPU ",
            "state": " alarm ",
            "region": " us-east-1 ",
        })

        self.assertEqual(result["alarm_name"], "HighCPU")
        self.assertEqual(result["state"], "ALARM")
        self.assertEqual(result["region"], "us-east-1")
        self.assertEqual(result["severity"], "P2")

    def test_invalid_optional_fields_fail(self):
        base_event = {
            "alarm_name": "HighCPU",
            "state": "ALARM",
            "region": "us-east-1",
        }

        invalid_fields = (
            ("resource_id", ""),
            ("resource_id", 123),
            ("incident_id", "   "),
            ("incident_id", None),
            ("summary", ""),
            ("summary", 123),
        )

        for field, value in invalid_fields:
            with self.subTest(field=field, value=value):
                event = {**base_event, field: value}
                with self.assertRaises(ValueError):
                    handler(event)


if __name__ == "__main__":
    unittest.main()
