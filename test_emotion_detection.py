"""Unit tests for the emotion_detector function."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import EmotionDetectorError, emotion_detector
from EmotionDetection.emotion_detection import WATSON_NLP_URL


class EmotionDetectorTests(unittest.TestCase):
    """Test successful, empty-input, and failure scenarios."""

    def setUp(self):
        self.scores = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.90,
            "sadness": 0.04,
        }
        self.response = Mock()
        self.response.status_code = 200
        self.response.json.return_value = {
            "emotionPredictions": [{"emotion": self.scores}]
        }
        self.response.raise_for_status.return_value = None

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_scores_and_dominant_emotion(self, mock_post):
        mock_post.return_value = self.response

        result = emotion_detector("I am happy.")

        self.assertEqual(result["dominant_emotion"], "joy")
        for emotion, score in self.scores.items():
            self.assertEqual(result[emotion], score)
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.args[0], WATSON_NLP_URL)
        self.assertEqual(
            mock_post.call_args.kwargs["json"],
            {"raw_document": {"text": "I am happy."}},
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_text_returns_none_values_without_request(self, mock_post):
        result = emotion_detector("   ")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(result[name] is None for name in self.scores))
        mock_post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none_values(self, mock_post):
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response

        result = emotion_detector("Text rejected by service")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(result[name] is None for name in self.scores))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_network_error_raises_domain_exception(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("offline")

        with self.assertRaises(EmotionDetectorError):
            emotion_detector("Some text")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_invalid_service_payload_raises_domain_exception(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {"unexpected": "payload"}
        mock_post.return_value = response

        with self.assertRaises(EmotionDetectorError):
            emotion_detector("Some text")


if __name__ == "__main__":
    unittest.main(verbosity=2)
