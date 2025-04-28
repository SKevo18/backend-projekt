import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.settings import get_setting


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
