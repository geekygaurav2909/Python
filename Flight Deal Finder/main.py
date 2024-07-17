import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import get_cheap_flight
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# setting up default origin airport to LON
ORIGIN_CITY_IATA = "LHR"

sheet_content = DataManager()
flight_search = FlightSearch()
notify_manager = NotificationManager()
sheet_data = sheet_content.get_destination_data()


# City code updater in the sheet, if data exists then only process it.
if sheet_content.codenull_data:
    for city in sheet_content.codenull_data:
        for city_id, city_name in city.items():
            iata_code = flight_search.get_iata_code(city_name)
            sheet_content.update_city_code(city_code=iata_code, row_id=city_id)

# --------- Getting user mailer lists ------ #
mailer_list = sheet_content.get_customer_emails()

# --------- Search for flights ----- #
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    flights = flight_search.check_flights(
        origin_city=ORIGIN_CITY_IATA,
        destination_city=destination["iataCode"],
        depart_date=tomorrow,
        return_date=six_months_from_today
    )
    cheapest_flight = get_cheap_flight(flights)
    print(f"{destination["city"]}: £{cheapest_flight.price}")
    # Slowing down the request to avoid limit
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        no_direct_flights = flight_search.check_flights(
            origin_city=ORIGIN_CITY_IATA,
            destination_city=destination["iataCode"],
            depart_date=tomorrow,
            return_date=six_months_from_today,
            is_direct=False
        )
        cheapest_flight = get_cheap_flight(no_direct_flights)
        print(f"{destination["city"]}: £{cheapest_flight.price}")

    try:
        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
            msg_body = (f"Low price alert! Only £{cheapest_flight.price} to fly from {ORIGIN_CITY_IATA} to "
                        f"{destination["city"]}, on {cheapest_flight.departure_date} "
                        f"untill {cheapest_flight.return_date}.")

            # notify_manager.send_message(msg_body)
            notify_manager.send_emails(recipient_email=mailer_list,
                                       email_content=msg_body)
    except TypeError:
        print(f"No flight between {ORIGIN_CITY_IATA} and {destination["city"]}")
