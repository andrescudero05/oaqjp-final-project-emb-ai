# Final Project

A Python application that estimates five emotions in English text using the IBM Watson NLP emotion service. It exposes a reusable `EmotionDetection` package, a Flask web interface, a JSON endpoint, unit tests, and basic error handling.

## Features

- Detects anger, disgust, fear, joy, and sadness.
- Returns the five scores and `dominant_emotion` in a predictable dictionary format.
- Makes the detector importable from the `EmotionDetection` package.
- Provides a Flask web page and JSON API endpoint.
- Handles blank input, HTTP 400 responses, network failures, HTTP errors, and malformed responses.
- Includes unit tests that mock the external service, so the main tests do not depend on network access.

## Requirements

- Python 3.10 or newer
- Internet access when making a real prediction through the Watson NLP service

## Run locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the unit tests

```bash
python -m unittest -v
```

The unit tests mock Watson NLP, so a working external connection is not required for this step.

### 4. Start the Flask application

```bash
python server.py
```

Open http://127.0.0.1:5000 in a browser. Enter an English statement and select **Analyze emotions**.

## Endpoints

- `GET /` - renders the web interface.
- `GET /emotionDetector?textToAnalyze=I%20am%20happy` - returns a human-readable result suitable for the web interface.
- `GET /api/emotionDetector?textToAnalyze=I%20am%20happy` - returns a JSON object with all five scores and the dominant emotion.

The API uses the Watson NLP endpoint provided for the course. Its availability may depend on the course lab environment and service availability.

## Example Python usage

```python
from EmotionDetection import emotion_detector

result = emotion_detector("I am so happy to be here!")
print(result)
print(result["dominant_emotion"])
```

A successful result has this shape (the actual scores depend on the input and model):

```python
{
    "anger": 0.01,
    "disgust": 0.02,
    "fear": 0.03,
    "joy": 0.90,
    "sadness": 0.04,
    "dominant_emotion": "joy",
}
```

## Static code analysis

Install the development dependencies and run Pylint:

```bash
python -m pip install -r requirements-dev.txt
pylint server.py EmotionDetection test_emotion_detection.py
```

Review the Pylint output and resolve any findings before submitting. The exact score may vary by Pylint version.

## Suggested GitHub submission checklist

1. Create a **public** GitHub repository for this project.
2. Commit the source files and this README.
3. Replace this checklist with the real public links to your repository's `README.md`, `EmotionDetection/emotion_detection.py`, and `EmotionDetection/__init__.py` when submitting the assignment.
4. Save screenshots or terminal output showing the unit tests passing, an import smoke test, a successful prediction in the course environment, the Flask interface running, and the Pylint results.

This local project does not publish itself to GitHub; the repository URL must be the one you create and push.
