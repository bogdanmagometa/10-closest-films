"""
main.py

The main module of the project for generating 10 closest locations of films shot in specified year.
In order to run user interface of the project, run this module.
"""

import math
from typing import Tuple, List
import time

import folium
from folium.plugins import FloatImage
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from urllib.request import urlretrieve


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


def get_coords_from_address(geocoder: Nominatim, address: str) -> Tuple[float, float]:
    """
    Return coordinates (lattitude and longitude) of the place represented by a given address.
    """

    try:
        location = geocoder.geocode(address)
    except GeocoderUnavailable:
        print("Exception run! Uraaaa!")
        return None

    if location:
        return location.latitude, location.longitude

    return None


def get_ten_closest(data: pd.DataFrame, coords) -> List[Tuple[str, Tuple[float, float]]]:
    """
    Return 10 films with closest location to the specified location.
    """

    data = data.sample(frac=1)

    # time to wait in seconds
    max_wait = 180

    coords_dict = {}

    start = time.time()
    films = []

    geocoder = Nominatim(user_agent="application_maps")

    for _, row in data.iterrows():

        if row[0] not in coords_dict:
            print('\n\n\n\n')
            print(row[2])
            coords_dict[row[0]] = get_coords_from_address(geocoder, row[2])

        film_location = coords_dict[row[0]]

        if not film_location:
            continue

        dist = calc_distance(film_location, coords)

        films.append((dist, (row[0], film_location)))

        if (time.time() - start) > max_wait:
            break
        time.sleep(0.7)

    try:
        films.sort()
    except:
        print(*films, sep='\n')

    return list(map(lambda x: x[1], films))[:10]


def generate_map(year: int, lat: float, lon: float) -> str:
    """
    Generate a map containing 10 closest locations of films shot in a given year to the specified
    location given by lat (lattitule) and lon (longitude). Save the map to html file. Return the
    name of the file.
    """

    data = pd.read_csv('locations.csv', header=None)
    data = data[data[1] == year]

    fol_map = folium.Map(location=[lat, lon], zoom_start=10)
    fg_ten_closest = folium.FeatureGroup(name="10 closest locations of films")

    # ten_closest = get_ten_closest(data, (lat, lon))
    print('ten_closest:')
    # print(*ten_closest, sep='\n')

    # for film in ten_closest:
        # fg_ten_closest.add_child(folium.Marker(location=film[1], popup=film[0]))

    fol_map.add_child(create_additional_layer('./world.json'))
    fol_map.add_child(fg_ten_closest)
    fol_map.add_child(folium.LayerControl())

    name_file = f"{year}_movies_map.html"
    fol_map.save(name_file)

    return name_file


def create_additional_layer(path: str) -> folium.FeatureGroup:
    """
    Create and return feature group
    """

    urlretrieve('https://hub.jovian.ml/wp-content/uploads/2020/09/countries.csv', 'countries.csv')

    data = pd.read_csv('countries.csv', usecols=['location', 'gdp_per_capita'])
    data.set_index('location', inplace=True)

    fg_gdp = folium.FeatureGroup(name='GDP per capita (09/2020)')

    def style_func(x):
        name = x['properties']['NAME']

        quantile_25 = data['gdp_per_capita'].quantile(0.25)
        quantile_50 = data['gdp_per_capita'].quantile(0.5)
        quantile_75 = data['gdp_per_capita'].quantile(0.75)

        try:
            cur_gdp = data.loc[name, 'gdp_per_capita']
        except KeyError:
            return {'fillColor': 'white', 'fillOpacity': 1}

        if cur_gdp < quantile_25:
            return {'fillColor': 'black', 'fillOpacity': 1}
        elif quantile_25 <= cur_gdp <= quantile_50:
            return {'fillColor': 'red', 'fillOpacity': 1}
        elif quantile_50 < cur_gdp <= quantile_75:
            return {'fillColor': 'orange', 'fillOpacity': 1}
        else:
            return {'fillColor': 'green', 'fillOpacity': 1}

    world_json = folium.GeoJson(data=open(path, 'r', encoding='utf-8-sig').read(),
                                                            style_function=style_func)

    image_fname = 'legend.png'

    fg_gdp.add_child(FloatImage(image_fname, bottom=1.5, left=63))
    fg_gdp.add_child(world_json)

    return fg_gdp


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
