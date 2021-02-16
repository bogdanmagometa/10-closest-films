"""
main.py

The main module of the project for generating 10 closest locations of films shot in specified year.
In order to run user interface of the project, run this module.
"""

import math
from typing import Tuple, List

import folium
import pandas as pd
from geopy.geocoders import Nominatim


def haversin(arg: float) -> float:
    """
    Return haversine of the given argument. Argument should be given in radians.

    >>> haversin(1)
    0.22984884706593015
    >>> haversin(-3.14)
    0.9999993658637698
    >>> haversin(1.552)
    0.49060238999094163
    >>> haversin(0)
    0.0
    """

    return math.sin(arg/2)**2


def calc_distance(location1: Tuple, location2: tuple) -> float:
    """
    Return the orthodromic distance (in km) between two points on Earth represented by tuples,
    containing latitude and longitude, location1 and location2.

    >>> calc_distance((139.74477, 35.6544), (39.8261, 21.4225))
    10994.283880585657
    >>> round(calc_distance((1, 1), (2, 2)))
    157
    >>> round(calc_distance((1.21, 32.1), (2, 89.5342)))
    6384
    >>> round(calc_distance((502.2, 502.2), (502.2, 502.2)))
    0
    >>> round(calc_distance((-26.6474403,-62.8121532), (-23.5459553,-48.9937375)))
    1433
    >>> round(calc_distance((-24.3766797,-64.1514063), (47.7116713,29.9257437)), -2)
    12300.0
    >>> round(calc_distance((70.1407185,-35.9671949), (-59.8096533,130.0329613)), -2)
    18700.0
    """

    lat1, lon1 = map(lambda x: float(x)*math.pi/180, location1)
    lat2, lon2 = map(lambda x: float(x)*math.pi/180, location2)

    # radius of Earth in kilometers
    earth_radius = 6_371

    haver = haversin(lat1-lat2) + math.cos(lat1)*math.cos(lat2)*haversin(lon2-lon1)

    dist = 2*earth_radius*math.asin(math.sqrt(haver))

    return dist


def get_coords_from_address(address: str) -> Tuple[float, float]:
    """
    Return coordinates (lattitude and longitude) of the place represented by a given address.
    """

    geocoder = Nominatim(user_agent="find_coords")
    location = geocoder.geocode(address)

    if location:
        return location.latitude, location.longitude

    return None


def get_ten_closest(data: pd.DataFrame, coords) -> Tuple[str, Tuple[float, float]]:
    """
    Return 10 closest locations of films to the specified location.
    """

    pass


def generate_map(year: int, lat: float, lon: float) -> str:
    """
    Generate a map containing 10 closest locations of films shot in a given year to the specified
    location given by lat (lattitule) and lon (longitude). Save the map to html file. Return the
    name of the file.
    """

    fol_map = folium.Map(location=[lat, lon], zoom_start=10)

    fg_ten_closest = folium.FeatureGroup(name="10 closest locations of films")

    data = pd.read_csv('locations.csv', header=None)
    data = data[data[2] == year]

    name_file = f"{year}_movies_map.html"
    fol_map.save(name_file)

    return name_file


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    year = int(input("Please enter a year you would like to have a map for: "))
    location = input("Please enter your location (format: lat, long): ")
    lat, lon = map(float, location.split(','))

    print("Map is generating...")
    print("Please wait...")

    file_name = generate_map(year, lat, lon)

    print(f"Finished. Please have look at the map {file_name}")
