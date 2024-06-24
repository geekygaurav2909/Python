import requests as reqs
from twilio.rest import Client
import smtplib

api_url = "https://api.openweathermap.org/data/2.5/weather"
api_url_3hr = "https://api.openweathermap.org/data/2.5/forecast"

parameter = {
    "lat": 25.31,
    "lon": 82.97,
    "appid": "app id for openweather API",
    "units": "metric",
    "cnt": 5
}

response = reqs.get(url=api_url_3hr, params=parameter)
response.raise_for_status()

data = response.json()
my_data = data["list"]
print(my_data)

if any(rec["weather"][0]["id"] >= 700 for rec in my_data):
    msg = "No need of Umbrella"
else:
    msg = "Bring an Umbrella"

# Sending report through text message
account_sid = "your account sid"
auth_token = "auth token id"
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_="your twilio app number",
    body=msg,
    to="recipient number"
)

# Sending report through mail
mail = "Your mail ID"
token_id = "Your 16 digit pw"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=mail, password=token_id)
    connection.sendmail(from_addr=mail, to_addrs=mail, msg=f"Subject:Weather Report\n\n{msg}")


