"""
export.py — JSON payload builder and file exporter.

Assembles the ML-ready payload from the user's answers and persists
it as a JSON file inside the ``src/responses/`` directory.  Output
filenames use the Spanish date format (DD-MM-YYYY).
"""

import json
import os
from datetime import datetime
from pathlib import Path

from src.config import GENDER_MAP, PROJECT_NAME, PROJECT_VERSION
from src.questions import getQuestions
from src.scoring import computeDerivedFeatures


# ─── Resolve the responses directory relative to *this* file ──────
# This ensures files are always saved inside src/responses/ no
# matter which working directory the user launches Streamlit from.
_RESPONSES_DIR = Path(__file__).resolve().parent / "responses"


def buildJsonPayload(
    user_name: str,
    user_surname: str,
    user_email: str,
    gender: str,
    responses: dict,
    q1_predictions: dict = None,
    q2_responses: dict = None,
    q2_prediction: str = None,
) -> dict:
    """
    Assemble the complete ML-ready JSON payload.

    Args:
        user_name:    user's first name.
        user_surname: user's surname.
        user_email:   user's email address.
        gender:       selected gender string ("Male", "Female", "Other").
        responses:    dict mapping question IDs to Likert values (1–5) for Q1.
        q1_predictions: dict containing predicted field of study and satisfaction.
        q2_responses: dict mapping Q2 question IDs to Likert values.
        q2_prediction: the predicted engineering specialty.

    Returns:
        dict ready to be serialised as JSON.
    """
    derivedFeatures = computeDerivedFeatures(responses)
    questions = getQuestions()

    # Build the flat numeric vector expected by the ML pipeline:
    # [genderCode, q1, q2, …, q25]
    modelVector = (
        [GENDER_MAP[gender]]
        + [responses[q["id"]] for q in questions]
    )

    payload = {
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "timestamp": datetime.now().isoformat(),
        "user_metadata": {
            "name": user_name,
            "surname": user_surname,
            "email": user_email,
            "gender": gender,
            "gender_code": GENDER_MAP[gender],
        },
        "responses": responses,
        "derived_features": derivedFeatures,
        "model_ready_vector": modelVector,
    }

    if q1_predictions:
        payload["q1_prediction"] = q1_predictions

    if q2_responses:
        from src.questions import getQuestionsQ2
        q2_questions = getQuestionsQ2()
        q2_vector = [q2_responses[q["id"]] for q in q2_questions]
        payload["q2_responses"] = q2_responses
        payload["q2_model_ready_vector"] = q2_vector
        if q2_prediction:
            payload["q2_prediction"] = q2_prediction

    return payload


def saveResponse(payload: dict) -> str:
    """
    Persist a completed questionnaire payload to disk as JSON.

    The filename uses the Spanish date format DD-MM-YYYY and a
    compact 24-hour time stamp:
        response_08-05-2026_21-19-42.json

    Args:
        payload: the dict returned by ``buildJsonPayload``.

    Returns:
        The relative file path of the saved JSON (for display).
    """
    # Ensure the output directory exists
    os.makedirs(_RESPONSES_DIR, exist_ok=True)

    # Format timestamp: DD-MM-YYYY_HH-MM-SS (Spanish date order)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    fileName = f"response_{timestamp}.json"
    filePath = _RESPONSES_DIR / fileName

    # Write the JSON with readable indentation and full Unicode
    with open(filePath, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return str(filePath)
