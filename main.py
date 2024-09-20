import json
import requests
from bs4 import BeautifulSoup

from key_lookup import *
from keys import MAPS_PLATFORM_API_KEY
from datetime import datetime

def format_leg(steps):
    """
    Formats single route (leg)
    :param steps:
    :return:
    """
    formatted_route = []

    for step in steps:
        if step:
            transit_details = step[TRANSIT_DETAILS]
            stops = transit_details[STOP_DETAILS]
            start_stop = stops[DEPARTURE_STOP]['name']
            end_stop = stops[ARRIVAL_STOP]['name']
            mode_of_transport = transit_details[TRANSIT_LINE]['name']
            num_stops = transit_details[STOP_COUNT]

            arrival_time = stops[ARRIVAL_TIME]
            departure_time = stops[DEPARTURE_TIME]
            dt_object = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%SZ")
            dt_object_b = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%SZ")

            time_difference = dt_object - dt_object_b

            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            formatted_route.append(
                {
                    'start_stop': start_stop,
                    'end_stop': end_stop,
                    'mode_of_transport': mode_of_transport,
                    'num_stops': num_stops,
                    'duration': f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                }
            )


    return formatted_route

def get_routes_from_address(start_address, end_address):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    payload = {
        "origin": {
            "address": start_address
        },
        "destination": {
            "address": end_address
        },
        "travelMode": "TRANSIT",
        "computeAlternativeRoutes": True,
        "transitPreferences": {
            "routingPreference": "FEWER_TRANSFERS",
            "allowedTravelModes": ["TRAIN"]
        }
    }

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": MAPS_PLATFORM_API_KEY,  # Replace with your actual API key
        "X-Goog-FieldMask": "routes.legs.steps.transitDetails"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Print the response
    return response.json()['routes']

def get_address_from_link(link):
    """
    Gets address from streeteasy webpage
    :param link: streeteasy webpage link
    :return: address string
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    response = requests.get(link, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    address = soup.findAll("title")[0].text
    idx1 = address.index('|')
    return address[:idx1]


if __name__ == '__main__':
    # For testing purposes
    # urls = [
    #     'https://streeteasy.com/building/28_30-jackson-avenue-long_island_city/45m?featured=1',
    #     'https://streeteasy.com/building/lucent33-condominium/4i?featured=1',
    #     'https://streeteasy.com/building/5241-center-boulevard-long_island_city/2905?featured=1',
    #     'https://streeteasy.com/building/skyline-tower/rental/4542429'
    # ]

    url = input('Enter URL: ')
    starting_address = input('Enter starting address: ')
    address_from_streeteasy = get_address_from_link(url)

    routes = get_routes_from_address(start_address=starting_address, end_address=address_from_streeteasy)

    for route in routes:
        legs = route['legs']
        for leg in legs:
            steps = leg['steps']
            print(format_leg(steps))