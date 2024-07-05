from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    def __init__(self, msg):
        self._sid = os.getenv("ACCOUNT_SID")
        self._key = os.getenv("AUTH_KEY")
        self.client = Client(self._sid, self._key)

        self.message = self.client.messages.create(
            from_=os.getenv("FROM_NUM"),
            body=msg,
            to=os.getenv("TO_NUM")
        )
