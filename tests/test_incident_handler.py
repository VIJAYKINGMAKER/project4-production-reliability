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


if __name__ == "__main__":
    unittest.main()
