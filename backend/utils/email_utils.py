import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()

# LOGGER
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Send email using GMAIL SMTP server
SENDER_MAIL = os.getenv("EMAIL_USER", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Check if SMTP settings are properly set
if not SMTP_HOST:
    logging.error("SMTP host is not set. Please configure 'SMTP_HOST' in your environment variables.")
if not SENDER_MAIL:
    logging.error("Sender email (EMAIL_USER) is not set.")
if not SMTP_PORT:
    logging.error("SMTP port is not set.")
if not PASSWORD:
    logging.error("Google App Password is not set.")


# function to send email
def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_MAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_MAIL, PASSWORD)
            server.sendmail(msg["From"], [to_email], msg.as_string())
        logging.info(f"Email sent to {to_email} with subject '{subject}'")
    except Exception as e:
        logging.error(f"Email send failed to {to_email}: {e}")