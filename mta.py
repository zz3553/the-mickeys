import requests
from nyct_gtfs.compiled_gtfs import nyct_subway_pb2, gtfs_realtime_pb2
from nyct_gtfs.gtfs_static_types import TripShapes, Stations
from nyct_gtfs.trip import Trip
url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"

response = requests.get(url)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
print(feed)