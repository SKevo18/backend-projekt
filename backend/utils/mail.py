import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from db import DB
from db.orm import Setting
from dotenv import load_dotenv

load_dotenv()


def get_setting(key: str) -> str | None:
    with DB.get_session() as session:
        setting = session.query(Setting).filter_by(key=key).first()
        return setting.value if setting else None


def send_email(recipient: str, subject: str, body: str):
    SMTP_SERVER = get_setting("smtp_host")
    SMTP_PORT = int(get_setting("smtp_port") or -1)
    EMAIL_SENDER = get_setting("email_sender")
    EMAIL_PASSWORD = get_setting("email_password")

    if SMTP_SERVER is None or SMTP_PORT == -1 or EMAIL_SENDER is None or EMAIL_PASSWORD is None:
        raise ValueError("SMTP server, port, sender email, or password is not set")

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
