import requests as reqs
import datetime as dt
import smtplib

MY_LAT = -25.317644
MY_LNG = 72.973915

api_url = "https://api.sunrise-sunset.org/json"
json_url = "http://api.open-notify.org/iss-now.json"
mail = "xyz@gmail.com"


# Checking and comparing position with ISS Position
def is_iss_overhead(long, lati):
    iss_response = reqs.get(url=json_url)
    iss_response.raise_for_status()

    iss_data = iss_response.json()

    longitude = float(iss_data["iss_position"]["longitude"])
    latitude = float(iss_data["iss_position"]["latitude"])

    return (long - 5 <= longitude <= long + 5) and (lati - 5 <= latitude < lati + 5)


def is_night():
    parameter = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
        "tzid": "Asia/Kolkata"
    }

    response = reqs.get(url=api_url, params=parameter)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


if is_iss_overhead(long=MY_LNG, lati=MY_LAT) and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=mail, password="xxxx xxxx xxxx xxxx")
        connection.sendmail(from_addr=mail, to_addrs=mail,
                            msg="Subject:ISS Overhead\n\nISS is crossing. do check that out.")
