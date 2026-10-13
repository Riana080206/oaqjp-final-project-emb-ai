"""Flask web application for emotion detection."""

from flask import Flask, render_template, request
import requests

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze text and return the detected emotions."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return "Please provide some text to analyze.", 400

    try:
        result = emotion_detector(text_to_analyze)
    except (requests.exceptions.RequestException, KeyError, ValueError):
        app.logger.exception("Emotion detection failed")
        return "Emotion detection service is unavailable.", 502

    if result["dominant_emotion"] is None:
        return "Emotion detection service is unavailable.", 502

    return (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
