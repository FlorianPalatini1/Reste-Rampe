"""
Email configuration for Reste-Rampe with Mailcow integration
"""
import os
from typing import Optional

# Mailcow SMTP Configuration
MAILCOW_SMTP_HOST = os.getenv("MAILCOW_SMTP_HOST", "mailcowdockerized-postfix-mailcow-1")
MAILCOW_SMTP_PORT = int(os.getenv("MAILCOW_SMTP_PORT", "587"))  # SMTP with TLS
MAILCOW_SMTP_USER = os.getenv("MAILCOW_SMTP_USER", "noreply@reste-rampe.tech")
MAILCOW_SMTP_PASSWORD = os.getenv("MAILCOW_SMTP_PASSWORD", "noreply")
MAILCOW_SMTP_TLS = os.getenv("MAILCOW_SMTP_TLS", "true").lower() == "true"

# Email Configuration
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@reste-rampe.tech")
FROM_NAME = os.getenv("FROM_NAME", "Reste-Rampe")

class EmailConfig:
    """Email configuration for SMTP"""
    SMTP_HOST = MAILCOW_SMTP_HOST
    SMTP_PORT = MAILCOW_SMTP_PORT
    SMTP_USER = MAILCOW_SMTP_USER
    SMTP_PASSWORD = MAILCOW_SMTP_PASSWORD
    SMTP_TLS = MAILCOW_SMTP_TLS
    FROM_EMAIL = FROM_EMAIL
    FROM_NAME = FROM_NAME

async def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Send email via Mailcow SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text email body
        html_body: Optional HTML email body
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        import smtplib
        import uuid
        from datetime import datetime
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{EmailConfig.FROM_NAME} <{EmailConfig.FROM_EMAIL}>"
        msg["To"] = to_email
        msg["Message-ID"] = f"<{uuid.uuid4()}@reste-rampe.tech>"
        msg["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
        
        # Add plain text part
        msg.attach(MIMEText(body, "plain"))
        
        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(EmailConfig.SMTP_HOST, EmailConfig.SMTP_PORT) as server:
            if EmailConfig.SMTP_TLS:
                server.starttls()
            server.login(EmailConfig.SMTP_USER, EmailConfig.SMTP_PASSWORD)
            server.sendmail(EmailConfig.FROM_EMAIL, to_email, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Email templates
class EmailTemplates:
    """Email templates for common tasks"""
    
    @staticmethod
    def welcome_email(username: str, email: str) -> tuple[str, str]:
        """Welcome email for new users"""
        subject = "Willkommen bei Reste-Rampe!"
        body = f"""Hallo {username},

willkommen bei Reste-Rampe! Dein Konto wurde erfolgreich erstellt.

Du kannst dich jetzt unter https://reste-rampe.tech anmelden.

Viel Erfolg!
Das Reste-Rampe Team"""
        
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
<h2>Willkommen bei Reste-Rampe!</h2>
<p>Hallo {username},</p>
<p>willkommen bei Reste-Rampe! Dein Konto wurde erfolgreich erstellt.</p>
<p><a href="https://reste-rampe.tech" style="background-color: #00CED1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Jetzt anmelden</a></p>
<p>Das Reste-Rampe Team</p>
</body>
</html>"""
        
        return subject, body, html_body
    
    @staticmethod
    def password_reset_email(username: str, reset_link: str) -> tuple[str, str]:
        """Password reset email"""
        subject = "Passwort zurücksetzen - Reste-Rampe"
        body = f"""Hallo {username},

du hast eine Anfrage zum Zurücksetzen deines Passworts gestellt.

Klicke auf den folgenden Link, um dein Passwort zu ändern:
{reset_link}

Dieser Link ist 24 Stunden gültig.

Das Reste-Rampe Team"""
        
        html_body = f"""<html>
<body style="font-family: Arial, sans-serif;">
<h2>Passwort zurücksetzen</h2>
<p>Hallo {username},</p>
<p>du hast eine Anfrage zum Zurücksetzen deines Passworts gestellt.</p>
<p><a href="{reset_link}" style="background-color: #00CED1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Passwort zurücksetzen</a></p>
<p><em>Dieser Link ist 24 Stunden gültig.</em></p>
<p>Das Reste-Rampe Team</p>
</body>
</html>"""
        
        return subject, body, html_body
