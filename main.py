import requests
from bs4 import BeautifulSoup
import sys

# headers = {
#     'Authorization':f"Bearer {MAPS_PLATFORM_API_KEY}",
#     'X-Goog-FieldMask': 'routes.routeToken,routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
# }
# req = \
#     f"https://routes.googleapis.com/directions/v2:computeRoutes"
#
# resp = requests.post(req, params=headers)
#
# print(resp.text)

def get_address_from_streeteasy(link):
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
    urls = [
        'https://streeteasy.com/building/28_30-jackson-avenue-long_island_city/45m?featured=1',
        'https://streeteasy.com/building/lucent33-condominium/4i?featured=1',
        'https://streeteasy.com/building/5241-center-boulevard-long_island_city/2905?featured=1',
        'https://streeteasy.com/building/skyline-tower/rental/4542429'
    ]
    url = input('Enter URL: ')
    print(get_address_from_streeteasy(url))