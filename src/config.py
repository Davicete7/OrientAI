"""
config.py — Application-wide constants and metadata.

Centralises every magic string, mapping, and label used across the
OrientAI application so they can be maintained in a single place.
"""

# ─── Project metadata ─────────────────────────────────────────────
PROJECT_NAME = "ORIENT_AI"
PROJECT_VERSION = "1.0"

# ─── Gender options & numeric encoding ─────────────────────────────
# The encoding is used inside the ML-ready vector that gets exported.
GENDER_OPTIONS = ["— select —", "Male", "Female"]
GENDER_MAP = {"Male": 1, "Female": 2}



# ─── Likert-scale reference ───────────────────────────────────────
# Maps the numeric value (1–5) to a descriptive label shown to the user.
SCALE_LABELS = {
    1: "Strongly Dislike",
    2: "Dislike",
    3: "Neutral",
    4: "Enjoy",
    5: "Strongly Enjoy",
}



# ─── Star-rating colours (index 0 → score 1, index 4 → score 5) ──
STAR_COLORS = ["#f87171", "#fb923c", "#fbbf24", "#34d399", "#4f8ef7"]
