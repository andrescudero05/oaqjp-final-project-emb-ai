"""Package for the Watson NLP emotion detection application."""

# Import the application module as requested by the package-validation task.
from . import emotion_detection
from .emotion_detection import EmotionDetectorError, emotion_detector

__all__ = ["emotion_detection", "EmotionDetectorError", "emotion_detector"]
