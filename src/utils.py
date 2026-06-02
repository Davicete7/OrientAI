"""
utils.py — Shared utility functions for the OrientAI application.

Provides helpers for loading static assets (CSS) and HTML templates
from the filesystem, keeping presentation markup separated from
Python logic.
"""

from pathlib import Path

# ─── Base directories resolved relative to this file ──────────────
_SRC_DIR = Path(__file__).resolve().parent
_STATIC_DIR = _SRC_DIR / "static"
_TEMPLATES_DIR = _SRC_DIR / "templates"


def loadStaticFile(fileName: str) -> str:
    """
    Read and return the full contents of a static asset file.

    Args:
        fileName: name of the file inside ``src/static/``
                  (e.g. ``"styles.css"``).

    Returns:
        The raw file contents as a string.
    """
    filePath = _STATIC_DIR / fileName
    return filePath.read_text(encoding="utf-8")


def loadTemplate(fileName: str, **kwargs) -> str:
    """
    Load an HTML template and interpolate placeholders.

    Templates live in ``src/templates/`` and use Python's
    ``str.format()`` syntax for placeholders (e.g. ``{filePath}``).

    Args:
        fileName: name of the template file (e.g. ``"hero.html"``).
        **kwargs: named values to substitute into the template.

    Returns:
        The rendered HTML string ready for ``st.markdown()``.
    """
    filePath = _TEMPLATES_DIR / fileName
    rawHtml = filePath.read_text(encoding="utf-8")

    # Only format if there are placeholders to fill
    if kwargs:
        return rawHtml.format(**kwargs)

    return rawHtml
