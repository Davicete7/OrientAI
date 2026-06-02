"""
results.py — Results / thank-you screen for the OrientAI application.

Displayed after a successful questionnaire submission.
"""

import streamlit as st

from src.utils import loadTemplate

# Map predicted fields/specialties to their official links from assets/Links/LinksToDegrees.pdf
Q1_LINKS = {
    "Arts": [
        ("Academy of Fine Arts", "https://www.asp.lodz.pl/index.php/pl/#headingStudents"),
        ("Łódź Film School", "https://www.filmschool.lodz.pl/en/")
    ],
    "Health": [
        ("Medical University of Lodz", "https://en.umed.pl/studies/")
    ],
    "Humanities": [
        ("University of Lodz (Faculty of Philology / Philosophy & History)", "https://www.uni.lodz.pl/en/ul-faculties-and-units")
    ],
    "Science": [
        ("University of Lodz & Lodz University of Technology", "https://www.uni.lodz.pl/en/ba-bachelors-degree")
    ],
    "Social Sciences": [
        ("University of Lodz (Faculty of Economics & Sociology / Law)", "https://www.uni.lodz.pl/en/ul-faculties-and-units")
    ],
    "Technologies": [
        ("Lodz University of Technology (TUL) Official Portal", "https://apply.p.lodz.pl/en/studyfield")
    ]
}

Q2_LINKS = {
    "Computer Science": [
        ("TUL Computer Science Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-computer-science")
    ],
    "Automatic Control and Robotics": [
        ("TUL Automatic Control and Robotics Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-automatic-control-and-robotics")
    ],
    "Automation and Robotics": [
        ("TUL Automation and Robotics Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-automation-and-robot-control")
    ],
    "Electrical Engineering": [
        ("TUL Electrical Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/second-cycle-electrical-engineering")
    ],
    "Civil Engineering": [
        ("TUL Civil Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-civil-engineering")
    ],
    "Architecture": [
        ("TUL Architecture Admission Portal (Polish)", "https://apply.p.lodz.pl/en/kierunek/first-cycle-architecture"),
        ("TUL Architecture Admission Portal (English)", "https://apply.p.lodz.pl/en/kierunek/first-cycle-architecture-english")
    ],
    "Chemistry": [
        ("TUL Chemistry Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-chemistry")
    ],
    "Nanotechnology": [
        ("TUL Nanotechnology Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-nanotechnology")
    ],
    "Biotechnology/biomedical engineering": [
        ("TUL Biomedical Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-biomedical-engineering"),
        ("TUL Biotechnology Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-biotechnology")
    ],
    "Environmental Engineering": [
        ("TUL Environmental Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-environmental-engineering")
    ],
    "Materials Engineering": [
        ("TUL Materials Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/second-cycle-materials-and-technologies")
    ],
    "Mechanical Engineering": [
        ("TUL Mechanical Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/second-cycle-mechanical-engineering")
    ],
    "Telecommunications": [
        ("TUL Electronic & Telecommunication Engineering Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-electronic-and-telecommunication-engineering"),
        ("TUL Electronics & Telecommunications Admission Portal", "https://apply.p.lodz.pl/en/kierunek/first-cycle-electronics-and-telecommunications")
    ],
    "Textile Technologies and Fashion Design": [
        ("TUL Textiles and Fashion Industry Admission Portal (Polish)", "https://apply.p.lodz.pl/en/kierunek/first-cycle-textiles-and-fashion-industry"),
        ("TUL Textiles and Fashion Industry Admission Portal (English)", "https://apply.p.lodz.pl/en/kierunek/first-cycle-textiles-and-fashion-industry-english")
    ]
}


def renderResults(payload: dict, filePath: str, is_intermediate: bool = False) -> None:
    """
    Render the post-submission results screen.

    Args:
        payload:  the full JSON payload dict.
        filePath: path where the JSON file was saved (for display).
        is_intermediate: True if this is the Q1 "Technology" result screen
                         before continuing to Q2.
    """
    # ── Personalized greeting ─────────────────────────────────────
    user_meta = payload.get("user_metadata", {})
    user_name = user_meta.get("name", "")
    user_surname = user_meta.get("surname", "")
    full_name = f"{user_name} {user_surname}".strip()

    if full_name and not is_intermediate:
        # Single-line compact HTML to avoid Python-Markdown block-split issues
        greeting_html = (
            '<div style="background:linear-gradient(135deg,rgba(99,102,241,0.12) 0%,rgba(16,185,129,0.08) 100%);border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;border:1px solid rgba(99,102,241,0.2);">'
            '<div style="display:flex;align-items:center;gap:1rem;">'
            '<div style="width:56px;height:56px;background:linear-gradient(135deg,#6366f1,#10b981);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.6rem;flex-shrink:0;">🎓</div>'
            '<div>'
            f'<h2 style="margin:0;font-size:1.6rem;font-weight:700;color:#1e293b;">Great job, {full_name}!</h2>'
            '<p style="margin:0.2rem 0 0 0;font-size:1rem;color:#64748b;">Your personalised academic orientation report is ready below.</p>'
            '</div></div></div>'
        )
        st.markdown(greeting_html, unsafe_allow_html=True)

    # ── Success banner ────────────────────────────────────────────
    if not is_intermediate:
        successHtml = loadTemplate("successBanner.html", filePath=filePath)
        st.markdown(successHtml, unsafe_allow_html=True)

    # ── AI Predictions ────────────────────────────────────────────
    q1_pred = payload.get("q1_prediction", {})
    q2_pred = payload.get("q2_prediction")
    field = q1_pred.get("field_of_study", "Unknown").title()
    satisfaction = q1_pred.get("predicted_satisfaction_score")

    if q1_pred:
        if is_intermediate:
            # ── Intermediate Q1→Q2 screen ─────────────────────────
            # Use compact single-line HTML to avoid Markdown splitting
            intermediate_html = (
                '<div class="card" style="border-left:4px solid #6366f1;">'
                '<div class="card-title">🤖 AI Career Prediction</div>'
                f'<p style="font-size:1.1rem;margin-top:10px;">Based on your responses, your ideal field of study is: <strong>{field}</strong></p>'
                '<div style="background-color:rgba(99,102,241,0.08);border-left:4px solid #6366f1;padding:1rem;margin-top:1rem;border-radius:4px;">'
                '<h4 style="margin:0 0 0.5rem 0;color:#3730a3;">Technology Profile Detected</h4>'
                '<p style="margin:0;font-size:0.95rem;color:#312e81;">Your interests strongly align with the Technology field. '
                '<strong>Please complete the next specific questionnaire</strong> to pinpoint the exact engineering degree that best suits you!</p>'
                '</div></div>'
            )
            st.markdown(intermediate_html, unsafe_allow_html=True)

            # Show satisfaction on intermediate screen too
            if satisfaction is not None:
                _renderSatisfactionBlock(satisfaction)

        else:
            # ── Final results screen hero block ───────────────────
            # Determine display field and links
            if q2_pred and q2_pred in Q2_LINKS:
                display_field = q2_pred
                links = Q2_LINKS[q2_pred]
            elif field in Q1_LINKS:
                display_field = field
                links = Q1_LINKS[field]
            else:
                display_field = field
                links = []

            # Build sub-snippets as single-line strings (no leading newlines).
            # This prevents Python-Markdown from treating blank lines inside
            # the outer <div> as block boundaries and escaping the inner HTML.
            links_html = "".join(
                f'<a href="{url}" target="_blank" style="display:inline-flex;align-items:center;gap:0.4rem;background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;text-decoration:none;padding:0.75rem 1.5rem;border-radius:10px;font-size:1rem;font-weight:600;margin:0.4rem 0.4rem 0 0;box-shadow:0 4px 14px rgba(99,102,241,0.35);">{name} &#x2197;</a>'
                for name, url in links
            )

            label = full_name if full_name else "you"

            # Single concatenated string — safe from Markdown block-split
            hero_html = (
                '<div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 60%,#0f172a 100%);border-radius:20px;padding:2.5rem 3rem;margin-bottom:1.5rem;text-align:center;border:1px solid rgba(99,102,241,0.3);box-shadow:0 8px 32px rgba(99,102,241,0.2);position:relative;overflow:hidden;">'
                '<div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;background:radial-gradient(circle,rgba(99,102,241,0.25) 0%,transparent 70%);border-radius:50%;"></div>'
                '<div style="position:relative;z-index:1;">'
                f'<p style="margin:0 0 0.6rem 0;font-size:1rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;font-weight:600;">&#x1F916; AI Career Prediction for {label}</p>'
                f'<h1 style="margin:0;font-size:3.2rem;font-weight:900;background:linear-gradient(135deg,#a5b4fc,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;">{display_field}</h1>'
                '<p style="margin:1.2rem 0 0.5rem 0;font-size:1rem;color:#cbd5e1;">Your ideal field of study based on your personality &amp; interests</p>'
                f'<div style="margin-top:1.2rem;">{links_html}</div>'
                '</div>'
                '</div>'
            )
            st.markdown(hero_html, unsafe_allow_html=True)

            # ── Satisfaction score block ──────────────────────────
            # Only show if not moving to or finishing Q2
            if satisfaction is not None and not q2_pred:
                _renderSatisfactionBlock(satisfaction)

            # ── Email confirmation box ────────────────────────────
            user_email = user_meta.get("email", "")
            email_display = user_email if user_email else "your email address"
            email_html = (
                '<div style="background:linear-gradient(135deg,rgba(16,185,129,0.08) 0%,rgba(99,102,241,0.06) 100%);border:1px solid rgba(16,185,129,0.3);border-radius:14px;padding:1.2rem 1.8rem;margin-top:1.2rem;display:flex;align-items:center;gap:1rem;">'
                '<div style="font-size:2rem;">&#x1F4E7;</div>'
                '<div>'
                '<div style="font-weight:700;font-size:1rem;color:#064e3b;">Results sent to your inbox!</div>'
                f'<div style="font-size:0.9rem;color:#475569;margin-top:0.15rem;">A personalised academic report has been sent to <strong>{email_display}</strong>. Please check your inbox (and spam folder) for your results.</div>'
                '</div></div>'
            )
            st.markdown(email_html, unsafe_allow_html=True)


def _renderSatisfactionBlock(satisfaction: float) -> None:
    """Render the predicted satisfaction score as a visual gauge block."""
    sat_pct = min(100, max(0, int(satisfaction)))

    if sat_pct >= 75:
        sat_colour = "#10b981"
        sat_text = "High Satisfaction"
        sat_emoji = "&#x1F31F;"
    elif sat_pct >= 50:
        sat_colour = "#f59e0b"
        sat_text = "Moderate Satisfaction"
        sat_emoji = "&#x1F60A;"
    else:
        sat_colour = "#ef4444"
        sat_text = "Room to Grow"
        sat_emoji = "&#x1F4AA;"

    # Also use single-line concatenation to prevent Markdown mis-parsing
    sat_html = (
        f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">'
        f'<div style="text-align:center;min-width:100px;">'
        f'<div style="font-size:0.8rem;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;font-weight:600;margin-bottom:0.3rem;">Field of study satisfaction</div>'
        f'<div style="font-size:3rem;font-weight:900;color:{sat_colour};line-height:1;">{sat_pct}<span style="font-size:1.2rem;color:#64748b;">/100</span></div>'
        f'<span style="display:inline-block;margin-top:0.4rem;background:rgba(0,0,0,0.15);border:1px solid {sat_colour};color:{sat_colour};border-radius:20px;padding:0.2rem 0.8rem;font-size:0.8rem;font-weight:600;">{sat_emoji} {sat_text}</span>'
        f'</div>'
        f'<div style="flex:1;min-width:200px;">'
        f'<div style="font-size:0.85rem;color:#94a3b8;margin-bottom:0.5rem;">Field of study satisfaction</div>'
        f'<div style="background:rgba(255,255,255,0.08);border-radius:8px;height:12px;overflow:hidden;">'
        f'<div style="background:linear-gradient(90deg,{sat_colour}88,{sat_colour});width:{sat_pct}%;height:100%;border-radius:8px;"></div>'
        f'</div>'
        f'<div style="font-size:0.8rem;color:#64748b;margin-top:0.4rem;">Based on academic profile analysis &mdash; how much you are likely to enjoy your chosen field.</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(sat_html, unsafe_allow_html=True)
