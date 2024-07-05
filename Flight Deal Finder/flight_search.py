import os
import requests as reqs
from dotenv import load_dotenv

load_dotenv()

FS_API_KEY = os.getenv("SEARCH_API_KEY")
FS_API_ID = os.getenv("SEARCH_API_ID")
FS_API_URL = "https://test.api.amadeus.com/v1"

GET_IATA_CODE = f"{FS_API_URL}/reference-data/locations/cities"
AUTH_TOKEN_GEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


main_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

key_params = {
    "client_id": FS_API_KEY,
    "client_secret": FS_API_ID,
    "grant_type": "client_credentials"
}


class FlightSearch:

    def __init__(self):
        self.response = reqs.post(url=AUTH_TOKEN_GEN_URL, data=key_params, headers=main_headers)
        self.token = self.response.json()
        self.auth_token = f"{self.token["token_type"]} {self.token["access_token"]}"

    def get_iata_code(self, city):
        search_param = {
            "keyword": city,
            "max": 1
        }

        search_header = {
            "Authorization": self.auth_token
        }
        iata_resp = reqs.get(url=GET_IATA_CODE, params=search_param, headers=search_header)
        content = iata_resp.json()
        try:
            code = content["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city, destination_city, depart_date, return_date):
        headers = {"Authorization": self.auth_token}
        query_param = {
            "originLocationCode": origin_city,
            "destinationLocationCode": destination_city,
            "departureDate": depart_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "nonStop": "true",
            "max": "10",
            "adults": 1,
            "currencyCode": "GBP"
        }

        search_resp = reqs.get(url=FLIGHT_ENDPOINT, headers=headers, params=query_param)

        if search_resp.status_code != 200:
            print(f"check_flights() response code: {search_resp.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", search_resp.text)
            return None

        return search_resp.json()
