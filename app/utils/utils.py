import math


def calculate_distance(lat1, long1, lat2, long2):
    """
    Calculates the Haversine distance between two sets of coordinates (latitude and longitude).

    Parameters:
    lat1, long1, lat2, long2 (float): Latitude and longitude of two points in degrees.

    Returns:
    distance (float): The Haversine distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    # Haversine formula
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = math.sin(
        dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of the Earth in kilometers
    radius = 6371.0

    # Calculate the Haversine distance
    distance = radius * c
    return distance
