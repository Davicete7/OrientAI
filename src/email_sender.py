"""
email_sender.py — Logic to send HTML email notifications with academic recommendations.

Reads SMTP configuration from environment variables and sends formatted emails
to survey respondents without requiring any paid API services.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st


def send_results_email(
    user_name: str,
    user_surname: str,
    user_email: str,
    field: str,
    specialty: str | None = None,
    satisfaction: float | None = None,
    links: list[tuple[str, str]] | None = None
) -> tuple[bool, str]:
    """
    Send an HTML-formatted academic orientation report to the user.

    Args:
        user_name:    First name of the user.
        user_surname: Surname of the user.
        user_email:   Destination email address.
        field:        Predicted general field of study (Q1 result).
        specialty:    Predicted technology specialty (Q2 result, if applicable).
        satisfaction: Predicted career satisfaction score (0–100).
        links:        List of (name, url) recommendation links to display.

    Returns:
        A tuple of (success_boolean, message_string).
    """
    full_name = f"{user_name} {user_surname}".strip()

    # ─── Load SMTP configuration from environment variables ─────────
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    sender_email = os.environ.get("SENDER_EMAIL")

    if not all([smtp_server, smtp_port, smtp_user, smtp_password, sender_email]):
        missing_vars = [
            var for var in ["SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SENDER_EMAIL"]
            if not os.environ.get(var)
        ]
        return False, f"Missing environment configuration for: {', '.join(missing_vars)}. Email notification skipped."

    try:
        port = int(smtp_port)
    except ValueError:
        return False, f"Invalid SMTP_PORT value: {smtp_port}. Must be an integer."

    # ─── Build Specialty block ───────────────────────────────────────
    display_field = specialty if specialty else field
    # ─── Build Satisfaction block ────────────────────────────────────
    satisfaction_html = ""
    if satisfaction is not None:
        sat_pct = min(100, max(0, int(satisfaction)))
        if sat_pct >= 75:
            sat_colour = "#10b981"
            sat_text = "High Satisfaction 🌟"
        elif sat_pct >= 50:
            sat_colour = "#f59e0b"
            sat_text = "Moderate Satisfaction 😊"
        else:
            sat_colour = "#ef4444"
            sat_text = "Room to Grow 💪"

        bar_width = sat_pct
        satisfaction_html = f"""
        <div style="background-color: #ffffff; border-radius: 8px; padding: 20px;
                    border: 1px solid #e2e8f0; margin-bottom: 20px; border-left: 4px solid {sat_colour};">
            <h3 style="color: {sat_colour}; margin-top: 0; font-size: 1.05rem;">📊 Field of study satisfaction</h3>
            <p style="font-size: 2rem; font-weight: 900; color: {sat_colour}; margin: 0 0 6px 0;">
                {sat_pct}<span style="font-size: 1rem; color: #94a3b8;">/100</span>
            </p>
            <div style="background: #e2e8f0; border-radius: 6px; height: 10px; overflow: hidden; margin-bottom: 8px;">
                <div style="background: {sat_colour}; width: {bar_width}%; height: 100%; border-radius: 6px;"></div>
            </div>
            <span style="font-size: 0.85rem; font-weight: 600; color: {sat_colour};">{sat_text}</span>
            <p style="font-size: 0.82rem; color: #64748b; margin: 6px 0 0 0;">
                This score estimates how much you are likely to enjoy working in your recommended field, based on your academic profile.
            </p>
        </div>
        """

    # ─── Build Links block ───────────────────────────────────────────
    links_html = ""
    if links:
        links_list_html = "".join([
            f'<li style="margin-bottom: 8px;"><a href="{url}" target="_blank" style="color: #6366f1; text-decoration: none; font-weight: 600;">{name} &rarr;</a></li>'
            for name, url in links
        ])
        links_html = f"""
        <div style="background-color: #ffffff; border-radius: 8px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px; border-left: 4px solid #10b981;">
            <h3 style="color: #10b981; margin-top: 0; font-size: 1.1rem;">🧭 Recommended Admission &amp; Study Program Links</h3>
            <p style="font-size: 0.95rem; margin-bottom: 10px;">Explore official degree options for your recommended profile in <strong>{display_field}</strong>:</p>
            <ul style="margin: 0; padding-left: 20px;">
                {links_list_html}
            </ul>
        </div>
        """

    # ─── Full HTML email body ────────────────────────────────────────
    html_body = f"""
    <html>
    <body style="background-color: #f1f5f9; padding: 20px; margin: 0; font-family: 'DM Sans', Arial, sans-serif;">
        <div style="background-color: #ffffff; padding: 36px; color: #334155; max-width: 620px; margin: 0 auto; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 24px rgba(0,0,0,0.06);">

            <!-- Header -->
            <h2 style="color: #6366f1; font-size: 1.5rem; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">
                🧭 ORIENT AI &mdash; Academic Report
            </h2>

            <!-- Greeting -->
            <p style="font-size: 1.05rem; line-height: 1.6; margin-bottom: 6px;">
                Hi <strong>{full_name}</strong>,
            </p>
            <p style="font-size: 1rem; line-height: 1.6; color: #475569;">
                Thank you for completing the OrientAI survey. We have analysed your responses and prepared your personalised academic orientation report below.
            </p>

            {satisfaction_html}

            <!-- Hero prediction -->
            <div style="
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                border-radius: 14px; padding: 28px 24px; margin-bottom: 24px; text-align: center;
                border: 1px solid rgba(99,102,241,0.3);
            ">
                <p style="margin: 0 0 6px 0; font-size: 0.8rem; color: #94a3b8; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600;">
                    🤖 AI Career Prediction for {full_name}
                </p>
                <h1 style="
                    margin: 0; font-size: 2.4rem; font-weight: 900; color: #a5b4fc; line-height: 1.1;
                ">{display_field}</h1>
                <p style="margin: 14px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
                    Your ideal field of study based on your personality &amp; interests
                </p>
            </div>

            {links_html}

            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
            <p style="font-size: 0.78rem; color: #94a3b8; text-align: center; margin: 0;">
                ORIENT AI Academic Advisor &middot; Lodz University of Technology
            </p>
        </div>
    </body>
    </html>
    """

    # ─── Set up MIMEMultipart message ────────────────────────────────
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"ORIENT AI — Academic Report for {full_name}"
    msg["From"] = sender_email
    msg["To"] = user_email

    msg.attach(MIMEText(html_body, "html"))

    # ─── Send via smtplib ───────────────────────────────────────────
    try:
        server = smtplib.SMTP(smtp_server, port, timeout=10)
        server.ehlo()
        if port == 587:
            server.starttls()
            server.ehlo()

        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()

        return True, "Email report sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
