"""
main.py

The main module of the project for generating 10 closest locations of films shot in specified year.
In order to run user interface of the project, run this module.
"""

import folium


def generate_map(year: int, lat: float, lon: float) -> str:
    """
    Generate a map containing 10 closest locations of films shot in a given year to the specified
    location given by lat (lattitule) and lon (longitude). Save the map to html file. Return the
    name of the file.
    """

    fol_map = folium.Map()

    name_file = f"{year}_movies_map.html"

    fol_map.save(name_file)

    return name_file


if __name__ == "__main__":
    year = int(input("Please enter a year you would like to have a map for: "))
    location = input("Please enter your location (format: lat, long): ")
    lat, lon = map(float, location.split(','))

    print("Map is generating...")
    print("Please wait...")

    file_name = generate_map(year, lat, lon)

    print(f"Finished. Please have look at the map {file_name}")
