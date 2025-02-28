import logging
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

with patch("logging.basicConfig"):
    from app.main import app


class TestMetricsEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

        cls.client = TestClient(app)

    @patch("app.services.metrics_service.MetricsService.get_metrics")
    def test_get_metrics_success(self, mock_get_metrics):
        mock_get_metrics.return_value = {
            "total_requests": 10,
            "success_count": 8,
            "error_count": 2,
            "request_rate": 1.5,
        }

        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "total_requests": 10,
                "success_count": 8,
                "error_count": 2,
                "request_rate": 1.5,
            },
        )

        mock_get_metrics.assert_called_once()

    @patch("app.services.metrics_service.MetricsService.get_metrics")
    def test_get_metrics_internal_error(self, mock_get_metrics):
        mock_get_metrics.side_effect = Exception("Internal error")

        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 500)
        self.assertEqual("An error occurred: Internal error", response.json()["detail"])
