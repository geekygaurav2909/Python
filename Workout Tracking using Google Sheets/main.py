import os
import requests as reqs
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Initial setup

GENDER = "Male"
WEIGHT_KG = 85
HEIGHT_CM = 175
AGE = 32

# Nutritionix API data
APP_ID = os.getenv("NUT_APP_ID")
API_KEY = os.getenv("NUT_API_KEY")
API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

header_auth_param = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

body_parameter = {
    "query": input("Tell me which exercises you did?: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = reqs.post(url=API_URL, json=body_parameter, headers=header_auth_param)
data = response.json()["exercises"]
# print(response.json())

# Sheety API Details
SHEETY_API_URL = os.getenv("SHT_END_POINT")
AUTH_KEY = os.getenv("AUTH_KEY")

sheety_auth_param = {
    "Content-Type": "application/json",
    "Authorization": AUTH_KEY
}

current_date = datetime.now()
date_format = current_date.strftime("%d/%m/%Y")
time = current_date.strftime("%H:%M:%S")

for content in data:
    sheety_workout_param = {
        "workout": {
            "date": date_format,
            "time": time,
            "exercise": content["name"].title(),
            "duration": content["duration_min"],
            "calories": content["nf_calories"]
        }
    }

    sheety_resp = reqs.post(url=SHEETY_API_URL, json=sheety_workout_param, headers=sheety_auth_param)
    # print(sheety_resp.text)
