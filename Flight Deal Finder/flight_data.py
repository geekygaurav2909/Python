class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_loc = origin_airport
        self.destination_loc = destination_airport
        self.departure_date = out_date
        self.return_date = return_date


def get_cheap_flight(data):

    if data is None or not data["data"]:
        print("No flight data available.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    source_port = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination_port = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, source_port, destination_port, out_date, return_date)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])

        if price < lowest_price:
            lowest_price = price
            source_port = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination_port = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, source_port, destination_port, out_date, return_date)
            print(f"Lowest price to {destination_port} is £{lowest_price}")

    return cheapest_flight

