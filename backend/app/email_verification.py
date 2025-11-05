"""Email verification utilities for user registration"""
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

MAILCOW_SMTP_HOST = os.getenv("MAILCOW_SMTP_HOST", "mailcow-postfix")
MAILCOW_SMTP_PORT = int(os.getenv("MAILCOW_SMTP_PORT", 587))
MAILCOW_SMTP_USER = os.getenv("MAILCOW_SMTP_USER", "noreply@reste-rampe.tech")
MAILCOW_SMTP_PASSWORD = os.getenv("MAILCOW_SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@reste-rampe.tech")
FROM_NAME = os.getenv("FROM_NAME", "Reste-Rampe")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://reste-rampe.tech")


def generate_verification_token() -> str:
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)


def send_verification_email(email: str, username: str, verification_token: str) -> bool:
    """
    Send verification email to user
    Returns True if successful, False otherwise
    """
    try:
        verification_link = f"{FRONTEND_URL}/verify-email?token={verification_token}"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Reste-Rampe - Bestätige deine Email"
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = email
        msg["Message-ID"] = f"<{secrets.token_hex(16)}@reste-rampe.tech>"
        msg["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0b1720;">Willkommen bei Reste-Rampe!</h2>
                <p>Hallo {username},</p>
                <p>danke, dass du dich bei Reste-Rampe registriert hast. Um dein Konto zu aktivieren, 
                bitte klicke auf den folgenden Link:</p>
                
                <p style="margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="display: inline-block; padding: 12px 30px; background-color: #0b1720; 
                              color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
                        Email bestätigen
                    </a>
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    Oder kopiere diesen Link in deinen Browser:<br>
                    <a href="{verification_link}" style="color: #0b1720; word-break: break-all;">
                        {verification_link}
                    </a>
                </p>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    Dieser Link ist 24 Stunden gültig.
                </p>
                
                <p style="color: #999; font-size: 12px;">
                    Das Reste-Rampe Team
                </p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Willkommen bei Reste-Rampe!
        
        Hallo {username},
        
        danke, dass du dich bei Reste-Rampe registriert hast. Um dein Konto zu aktivieren, 
        bitte kopiere diesen Link in deinen Browser:
        
        {verification_link}
        
        Dieser Link ist 24 Stunden gültig.
        
        Das Reste-Rampe Team
        """
        
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        # Send email
        with smtplib.SMTP(MAILCOW_SMTP_HOST, MAILCOW_SMTP_PORT) as server:
            server.starttls()
            server.login(MAILCOW_SMTP_USER, MAILCOW_SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    
    except Exception as e:
        print(f"Error sending verification email to {email}: {e}")
        return False
