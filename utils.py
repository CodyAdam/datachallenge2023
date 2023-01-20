import math


def geo_to_xy(geopoint):
    latitude, longitude = geopoint.split(',')
    latitude = float(latitude)
    longitude = float(longitude)

    center_latitude = 48.15260488650874
    center_longitude = -2.66515226998977
    # Convert latitude and longitude to radians
    latitude_rad = math.radians(latitude)
    longitude_rad = math.radians(longitude)
    center_latitude_rad = math.radians(center_latitude)
    center_longitude_rad = math.radians(center_longitude)

    # Calculate x and y coordinates
    x = (longitude_rad - center_longitude_rad) * math.cos(
        (center_latitude_rad + latitude_rad) / 2)
    y = latitude_rad - center_latitude_rad
    multi = 10000
    return (x * multi, y * multi)
