"""Tests for the AWS Lambda entry point."""

import unittest

from src.lambda_handler import lambda_handler


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


class LambdaHandlerTests(unittest.TestCase):
    def test_alarm_event_creates_p2_incident(self):
        result = lambda_handler(make_event("ALARM"), None)

        self.assertEqual(result["alarm_name"], "HighCPU")
        self.assertEqual(result["state"], "ALARM")
        self.assertEqual(result["severity"], "P2")
        self.assertEqual(result["region"], "us-east-1")
        self.assertEqual(result["resource_id"], "unknown")
        self.assertEqual(result["summary"], "Alarm threshold crossed")
        self.assertTrue(result["deduplication_key"])
        self.assertTrue(result["created_at"])

    def test_ok_event_creates_p3_incident(self):
        result = lambda_handler(make_event("OK"), None)

        self.assertEqual(result["state"], "OK")
        self.assertEqual(result["severity"], "P3")

    def test_invalid_event_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "dictionary"):
            lambda_handler(None, None)

    def test_missing_detail_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "detail dictionary"):
            lambda_handler({"region": "us-east-1"}, None)

    def test_unsupported_state_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ALARM or OK"):
            lambda_handler(make_event("INSUFFICIENT_DATA"), None)


if __name__ == "__main__":
    unittest.main()
