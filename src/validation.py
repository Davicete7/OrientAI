"""
validation.py — Form validation for the OrientAI questionnaire.

Checks that every required field has been answered and that all
values fall within the expected ranges before submission.
"""

from src.questions import getQuestions


def validateResponses(
    gender: str | None,
    responses: dict,
) -> list[str]:
    """
    Validate the full questionnaire submission.

    Returns a list of human-readable error messages.
    An empty list means all inputs are valid.
    """
    errors: list[str] = []

    # ── Gender must be selected ───────────────────────────────────
    if not gender:
        errors.append("Gender selection is required.")

    # ── Every question must have a value in the 1–5 range ─────────
    for question in getQuestions():
        value = responses.get(question["id"])

        if value is None:
            # Truncate long texts so the error message stays readable
            errors.append(f"Unanswered: «{question['text'][:60]}»")
        elif not (1 <= value <= 5):
            errors.append(f"Out of range: {question['id']} must be 1–5.")

    return errors
