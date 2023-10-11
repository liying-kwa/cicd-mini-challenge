import base64
import json
from app.model.Message import Message
from app.model.Station import Station
import app.utils.utils as utils


def read_json(json_file):
    """
    This function reads a JSON file and returns its content.

    Parameters:

        json_file (str): The path to the JSON file.

    Returns:

        dict: The content of the JSON file as a Python dictionary.
    """
    with open(json_file) as stream:
        json_file = json.load(stream)
    return json_file


def get_messages():
    messages = read_json("data/message.json")
    messages = [Message.parse_obj(message) for message in messages]
    return messages


def get_latlong(mrt_station: str, station_list: list[Station]):
    for station in station_list:
        if mrt_station == station.name:
            return station.get_latlong()
    raise ValueError(f"No station found with the name {mrt_station}")


def nearest_spooky_site(station_name: str):
    """
    Task: Find the spooky location with the nearest MRT station to the one specified
    TODO: fix function logic
    """

    # Get list of MRT stations
    mrt_stations = read_json("mrt.json")
    mrt_stations = [
        Station.parse_obj(mrt_station) for mrt_station in mrt_stations
    ]

    # Get the latitude and longitude of the specified station
    target_lat, target_lon = get_latlong(station_name, mrt_stations)

    # Get list of spooky locations
    spooky_locations = read_json("dat/haunted_location.json")

    closest_location = None
    closest_distance = float("inf")  # Initialize with a large value

    for location in spooky_locations:
        nearest_mrt = location["nearest_mrt"]
        # Get the latitude and longitude of the nearest MRT station to the spooky location
        lat, lon = get_latlong(nearest_mrt, mrt_stations)

        # Calculate the distance between the specified station and the nearest MRT station to the spooky location
        distance = utils.calculate_distance(lat, lon, target_lat, target_lon)

        # If this distance is less than the closest recorded so far, update the closest location and distance
        if distance > closest_distance:
            closest_distance = distance
            closest_location = location

    # Return the spooky location with the nearest MRT station to the specified station
    return closest_location


def print_secret():
    """
    This function returns a secret message.
    """
    return base64.b64decode(
        "Q1NJVCdzIHRlY2ggZm9jdXMgYXJlYXMgaW5jbHVkZSBDeWJlcnNlY3VyaXR5LCBTb2Z0d2FyZSBFbmdpbmVlcmluZywgRGF0YSBBbmFseXRpY3MsIGFuZCBDbG91ZCBJbmZyYXN0cnVjdHVyZSBhbmQgU2VydmljZXMu"
    )
