from twilio.rest import Client
import os
from dotenv import load_dotenv
from smtplib import SMTP

load_dotenv()


class NotificationManager:

    def __init__(self):
        self._sid = os.getenv("ACCOUNT_SID")
        self._key = os.getenv("AUTH_KEY")
        self._mail_id = os.getenv("MAIL_ID")
        self._pass = os.getenv("PASS")
        self.client = Client(self._sid, self._key)

    def send_message(self, msg):
        message = self.client.messages.create(
            from_=os.getenv("FROM_NUM"),
            body=msg,
            to=os.getenv("TO_NUM")
        )

    def send_emails(self, recipient_email, email_content):
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self._mail_id, password=self._pass)
            connection.sendmail(from_addr=self._mail_id,
                                to_addrs=recipient_email,
                                msg=f"Subject:Low Price Alert\n\n{email_content}".encode("utf-8"))
