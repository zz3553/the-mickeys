from keys import MAPS_PLATFORM_API_KEY
import requests

req = \
    f"https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key={MAPS_PLATFORM_API_KEY} "

resp = requests.get(req)

print(resp.json())
