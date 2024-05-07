from os import environ as ENV
from csv import DictWriter

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


def get_street_crimes_data(coords: tuple[float, float], year: int, month: int) -> list[dict]:
    """Given a location - (longitude, latitude) - this function returns
    data of street-level crimes within a 1 mile radius, for a specific
    year-month."""

    longitude, latitude = coords[0], coords[1]

    crime_data = requests.get(
        POLICE_BASE_URL+f"/crimes-street/all-crime?lat={latitude}&lng={longitude}&date={year}-{month}").json()

    return crime_data


def get_relevant_street_crimes_data(coords: tuple[float, float], year: int, month: int) -> list[dict]:
    """Given a location - (longitude, latitude) - this function returns
    RELEVANT data of street-level crimes within a 1 mile radius, for a specific
    year-month."""

    crime_data = get_street_crimes_data(coords, year, month)

    relevant_data = []
    for crime in crime_data:

        outcome_status = crime['outcome_status']['category'] if crime['outcome_status'] is not None else 'Unknown'
        relevant_data.append({'category': crime['category'], 'street name': crime['location']
                              ['street']['name'], 'outcome': outcome_status, 'date': crime['month']})

    return relevant_data


def crime_data_to_csv(data: list[dict], file_path: str):
    """Given a list of dictionaries with crime data, each dictionary
    representing a crime, this function outputs the data into a csv
    file."""

    with open(file_path, 'w') as f:
        field_names = data[0].keys()
        writer = DictWriter(f, fieldnames=field_names)
        writer.writeheader()

        for crime in data:
            writer.writerow(crime)


def get_stop_and_search_data(coords: tuple[float, float], year: int, month: int) -> list[dict]:
    """Given a location - (longitude, latitude) - this function returns
    data for stop and search instances within a 1 mile radius, for a specific
    year-month."""

    longitude, latitude = coords[0], coords[1]

    crime_data = requests.get(
        POLICE_BASE_URL+f"/stops-street?lat={latitude}&lng={longitude}&date={year}-{month}").json()

    return crime_data


if __name__ == "__main__":

    load_dotenv()

    coords = postcode_to_coords(ENV["MY_POSTCODE"])

    jan_crime_data = get_relevant_street_crimes_data(coords, 2024, 1)

    crime_data_to_csv(jan_crime_data, 'Jan 2024')

    ss_data = get_stop_and_search_data(coords, 2024, 1)

    print(ss_data[0])
