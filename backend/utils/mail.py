import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from db.orm import Setting
from typing import Optional


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_setting(key: str) -> Optional[str]:
    with Session(engine) as session:
        setting = session.query(Setting).filter_by(key=key).first()
        return setting.value if setting else None

def send_email(recipient: str, subject: str, body: str):
    try:
        SMTP_SERVER = get_setting("smtp_host")
        SMTP_PORT = int(get_setting("smtp_port"))
        EMAIL_SENDER = get_setting("email_sender")
        EMAIL_PASSWORD = get_setting("email_password")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.quit()

        print(f"Email sent to {recipient} from {EMAIL_SENDER}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
