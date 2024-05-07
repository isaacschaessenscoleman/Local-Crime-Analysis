from os import environ as ENV

import requests
from dotenv import load_dotenv


POSTCODE_BASE_URL = "https://api.postcodes.io"
POLICE_BASE_URL = "https://data.police.uk/api"


def postcode_to_coords(postcode: str) -> tuple[float]:
    """Given a postcode, this function returns corresponding
     geographic coordinates - (longitude, latitude)."""

    location_data = requests.get(
        POSTCODE_BASE_URL+f"/postcodes/{postcode}").json()

    if location_data['status'] != 200:
        raise Exception("Unsuccessful HTTP Request.")

    return (location_data['result']['longitude'], location_data['result']['latitude'])


def get_street_crimes_data(coords: tuple[float, float], year: int, month: int):
    """Given a location - (longitude, latitude) - this function returns
    data of street-level crimes within a 1 mile radius, for a specific
    year-month."""

    longitude, latitude = coords[0], coords[1]

    crime_data = requests.get(
        POLICE_BASE_URL+f"/crimes-street/all-crime?lat={latitude}&lng={longitude}&date={year}-{month}").json()

    return crime_data


if __name__ == "__main__":

    load_dotenv()

    coords = postcode_to_coords(ENV["MY_POSTCODE"])

    crime_data = get_street_crimes_data(coords, 2024, 2)
