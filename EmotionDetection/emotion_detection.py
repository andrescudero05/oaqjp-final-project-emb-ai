"""Detect emotions in text using the IBM Watson NLP emotion service."""

from __future__ import annotations

from typing import Any

import requests

WATSON_NLP_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
REQUEST_TIMEOUT_SECONDS = 15
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


class EmotionDetectorError(RuntimeError):
    """Raised when the Watson NLP service cannot return a valid prediction."""


def _empty_result() -> dict[str, float | str | None]:
    """Return the standard result shape when no prediction is available."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(
    text_to_analyze: str | None,
) -> dict[str, float | str | None]:
    """Return five emotion scores and the dominant emotion for a text.

    An empty input (or a Watson HTTP 400 response) returns the standard result
    dictionary with ``None`` values. Network failures, other HTTP errors, or
    malformed service responses raise :class:`EmotionDetectorError`.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_NLP_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise EmotionDetectorError(
            "No fue posible conectar con el servicio Watson NLP."
        ) from exc

    if response.status_code == 400:
        return _empty_result()

    try:
        response.raise_for_status()
        data: Any = response.json()
        predictions = data["emotionPredictions"]
        scores = predictions[0]["emotion"]

        normalized_scores = {
            emotion: float(scores[emotion]) for emotion in EMOTION_NAMES
        }
    except (requests.HTTPError, ValueError, KeyError, IndexError, TypeError) as exc:
        raise EmotionDetectorError(
            "Watson NLP devolvió una respuesta inesperada o no válida."
        ) from exc

    dominant_emotion = max(normalized_scores, key=normalized_scores.get)
    return {
        **normalized_scores,
        "dominant_emotion": dominant_emotion,
    }
