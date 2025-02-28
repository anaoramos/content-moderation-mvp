import logging
import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

with patch("logging.basicConfig"):
    from app.main import app


class TestModerateTextEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

        cls.client = TestClient(app)

    @patch("app.services.moderation_service.Predictor.load_model")
    @patch("app.services.moderation_service.Predictor.predict_moderation")
    def test_moderate_text_success(self, mock_predict_moderation, mock_load_model):
        mock_predict_moderation.return_value = {
            "text": "I hate you",
            "category": "hate",
            "confidence": 0.98,
        }

        mock_load_model.return_value = None

        response = self.client.post("/moderate", json={"text": "I hate you"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"text": "I hate you", "category": "hate", "confidence": 0.98},
        )

    @patch("app.routers.router.ModerationService.predict_moderation")
    def test_moderate_text_internal_error(self, mock_predict_moderation):
        mock_predict_moderation.side_effect = Exception("Internal error")

        response = self.client.post("/moderate", json={"text": "I hate you"})

        self.assertEqual(response.status_code, 500)
        self.assertIn("An error occurred", response.json()["detail"])

    def test_moderate_text_invalid_data(self):
        response = self.client.post("/moderate", json={})

        self.assertEqual(response.status_code, 422)
        self.assertIn(
            "{'detail': [{'type': 'missing', 'loc': ['body', 'text'], 'msg': 'Field required', 'input': {}}]}",
            str(response.json()),
        )
