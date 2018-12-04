import unirest
from time import sleep
import random

locations = {"Sydney": "SYDA-sky", "Amsterdam": "AMS-sky", "Melbourne": "MELA-sky", "Singapore": "SG-sky",
             "Adelaide": "ADL-sky"}


def get_locations(place_name):
    response = unirest.get(
        "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB"
        "/?query=" + place_name,
        headers={
            "X-RapidAPI-Key": "662386bdb7msh62ea12c0e29cd96p14ec15jsn6a15a255e88d"
        }
    )
    place_ids = [placeId for placeId in [dic["PlaceId"] for dic in response.body["Places"]]]

    return place_ids


def get_return_price(location_from, location_to, outbound, inbound):
    response = unirest.post("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
                            headers={
                                "X-RapidAPI-Key": "662386bdb7msh62ea12c0e29cd96p14ec15jsn6a15a255e88d",
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            params={
                                "children": 0,
                                "infants": 0,
                                "country": "US",
                                "currency": "EUR",
                                "locale": "en-US",
                                "originPlace": location_from,
                                "destinationPlace": location_to,
                                "inboundDate": inbound,
                                "outboundDate": outbound,
                                "adults": 1
                            }
                            )

    location_id = response.headers.get("location")[-36:]

    sleep(random.randint(1, 3))

    response = unirest.get(
        "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/" + location_id,
        headers={
            "X-RapidAPI-Key": "662386bdb7msh62ea12c0e29cd96p14ec15jsn6a15a255e88d"
        },
        params={
            "duration": 35 * 60 * 2,
            "sortType": "price",
            "sortOrder": "asc"
        }
    )

    return response.body["Itineraries"]


def get_single_price(location_from, location_to, outbound):
    response = unirest.post("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
                            headers={
                                "X-RapidAPI-Key": "662386bdb7msh62ea12c0e29cd96p14ec15jsn6a15a255e88d",
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            params={
                                "children": 0,
                                "infants": 0,
                                "country": "US",
                                "currency": "EUR",
                                "locale": "en-US",
                                "originPlace": location_from,
                                "destinationPlace": location_to,
                                "outboundDate": outbound,
                                "adults": 1
                            }
                            )

    location_id = response.headers.get("location")[-36:]

    sleep(random.randint(1, 3))

    response = unirest.get(
        "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/" + location_id,
        headers={
            "X-RapidAPI-Key": "662386bdb7msh62ea12c0e29cd96p14ec15jsn6a15a255e88d"
        },
        params={
            "duration": 35 * 60,
            "sortType": "price",
            "sortOrder": "asc"
        }
    )

    return response.body["Itineraries"]


def query_flights():
    queries = []
    # AMS-SYD-MEL-AMS
    query = []
    query.append(["Amsterdam", "Sydney", ["2019-06-24", "2019-06-25", "2019-06-26", "2019-06-27", "2019-06-28"]])
    query.append(["Melbourne", "Amsterdam", ["2019-07-23", "2019-07-24", "2019-07-25"]])
    queries.append(query)

    results = []
    for query in queries:
        sleep(random.randint(1, 2))
        price = 0
        for flight in query:
            sleep(random.randint(1, 2))
            flight_prices = []
            loc_from = flight[0]
            loc_to = flight[1]
            for date in flight[2]:
                sleep(random.randint(1, 2))
                flights = get_single_price(locations[loc_from], locations[loc_to], date)
                flight_prices.append(min([min(dic["Price"] for dic in flight["PricingOptions"]) for flight in flights]))

            price += min(flight_prices)

        results.append(price)

    return results


print(query_flights())
