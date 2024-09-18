import json
import requests
from bs4 import BeautifulSoup

from key_lookup import *
from keys import MAPS_PLATFORM_API_KEY
from steps_test_data import steps


def format_leg(steps):
    """
    Formats single route (leg)
    :param steps:
    :return:
    """
    formatted_route = []
    # [
    #     {
    #         'start_stop':'',
    #         'end_stop':'',
    #         'mode_of_transport':'',
    #         'num_stops':'',
    #     }, ...
    # ]
    for step in steps:
        if step:
            curr_transfer = step[TRANSIT_DETAILS]
            stops = curr_transfer[STOP_DETAILS]
            start_stop = stops[ARRIVAL_STOP]['name']
            end_stop = stops[DEPARTURE_STOP]['name']
            mode_of_transport = curr_transfer[TRANSIT_LINE]['name']
            num_stops = curr_transfer[STOP_COUNT]
            formatted_route.append(
                {
                    'start_stop': start_stop,
                    'end_stop': end_stop,
                    'mode_of_transport': mode_of_transport,
                    'num_stops': num_stops,
                }
            )


    return formatted_route

def get_route_from_address(start_address, end_address):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    # Define the payload (body of the request)
    payload = {
        "origin": {
            "address": "9308 177th St Jamaica, NY"
        },
        "destination": {
            "address": "Barclays Center"
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
    # leg: route
    # step: each transfer

    # Print the response
    print(response.json()['routes'])
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
    # url = input('Enter URL: ')
    # print(get_address_from_link(url))

    # get_route_from_address('', '')

    print(format_leg(steps))