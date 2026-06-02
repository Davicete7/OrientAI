"""
scoring.py — Derived features and satisfaction labelling.

Computes the average Likert score for each academic pillar.
"""

# ─── Pillar-to-question mapping ───────────────────────────────────
# Each key is the name that appears in the exported JSON under
# "derived_features"; each value is the list of question IDs
# whose scores are averaged to produce that pillar score.
# Updated to match the new question IDs in order of the PDF.
_PILLAR_QUESTIONS = {
    "creative_artistic_score": [
        "q1_1",
        "q1_3",
        "q1_11",
        "q1_16",
    ],
    "health_science_score": [
        "q1_2",
        "q1_9",
        "q1_18",
        "q1_22",
        "q1_24",
    ],
    "logical_technical_score": [
        "q1_4",
        "q1_6",
        "q1_8",
        "q1_12",
        "q1_14",
        "q1_17",
        "q1_23",
        "q1_25",
    ],
    "humanities_theory_score": [
        "q1_5",
        "q1_13",
        "q1_19",
        "q1_21",
    ],
    "social_institutional_score": [
        "q1_7",
        "q1_10",
        "q1_15",
        "q1_20",
    ],
}


def computeDerivedFeatures(responses: dict) -> dict:
    """
    Compute the average score (1.00–5.00) for each academic pillar.

    Args:
        responses: dict mapping question IDs to their Likert values (1–5).

    Returns:
        dict with pillar names as keys and rounded averages as values.
    """
    derivedFeatures = {}

    for pillarName, questionIds in _PILLAR_QUESTIONS.items():
        # Sum only the questions that exist in the response dict
        total = sum(responses[qId] for qId in questionIds if qId in responses)
        average = total / len(questionIds)
        derivedFeatures[pillarName] = round(average, 2)

    return derivedFeatures
