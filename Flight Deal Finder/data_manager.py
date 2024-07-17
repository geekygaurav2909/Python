import os
import requests as reqs
from dotenv import load_dotenv

load_dotenv()

SHEETY_URL = os.getenv("SHEETY_API_URL")
SHEETY_USERS_URL = os.getenv("SHEETY_USER_URL")


class DataManager:

    def __init__(self):
        self._token = os.getenv("SHEETY_TOKEN")
        self.sheety_headers = {
            "Authorization": self._token
        }
        self.response = reqs.get(url=SHEETY_URL, headers=self.sheety_headers)
        self.content = self.response.json()
        # iatacode null checker
        self.codenull_data = [{record["id"]: record["city"]} for record in self.content["prices"]
                              if record["iataCode"] == ""]
        self.destination_data = {}

        # Adding up users data
        self._user_token = os.getenv("SHEETY_USER_TOKEN")
        self.sheety_users_headers = {
            "Authorization": self._user_token
        }

    def get_destination_data(self):
        self.destination_data = self.content["prices"]
        return self.destination_data

    def update_city_code(self, city_code, row_id):
        body_param = {
            "price": {
                "iataCode": city_code,
            }
        }
        update_resp = reqs.put(url=f"{SHEETY_URL}/{row_id}", json=body_param, headers=self.sheety_headers)
        return update_resp.json()

    def get_customer_emails(self):
        user_response = reqs.get(url=SHEETY_USERS_URL, headers=self.sheety_users_headers)
        user_mail = user_response.json()["users"]
        email_data = [user["whatIsYourEmail?"] for user in user_mail]
        return email_data

