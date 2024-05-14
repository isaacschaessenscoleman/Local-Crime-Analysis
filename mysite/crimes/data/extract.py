'''This file contains all of the functions related to extracting data from the Police and Postcode
APIs.'''

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
        POLICE_BASE_URL+f"/crimes-street/all-crime?lat={latitude}&lng={longitude}&date={year}-{month}")

    if crime_data.status_code != 200:
        raise Exception(
            f'Unsuccessful request - Status Code: {crime_data.status_code}')

    return crime_data.json()


def get_relevant_street_crimes_data(coords: tuple[float, float], year: int, month: int) -> list[dict]:
    """Given a location - (longitude, latitude) - this function returns
    RELEVANT data of street-level crimes within a 1 mile radius, for a specific
    year-month."""

    crime_data = get_street_crimes_data(coords, year, month)

    relevant_data = []
    for crime in crime_data:

        outcome_status = crime['outcome_status']['category'] if crime['outcome_status'] is not None else 'Unknown'
        relevant_data.append({'category': crime['category'], 'street': crime['location']
                              ['street']['name'], 'outcome': outcome_status, 'date': crime['month']})

    return relevant_data


def dict_to_csv(data: list[dict], file_path: str) -> None:
    """Given a list of dictionaries with identical keys, representing an
    instance of something, this function outputs the data into a csv
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

    ss_data = requests.get(
        POLICE_BASE_URL+f"/stops-street?lat={latitude}&lng={longitude}&date={year}-{month}").json()

    return ss_data


def get_relevant_stop_and_search_data(coords: tuple[float, float], year: int, month: int) -> list[dict]:
    """Given a location - (longitude, latitude) - this function returns
    RELEVANT data for stop and search instances within a 1 mile radius, for a specific
    year-month."""

    ss_data = get_stop_and_search_data(coords, year, month)

    relevant_data = []
    for event in ss_data:

        relevant_data.append({'age range': event['age_range'], 'outcome': event['outcome'],
                              'involved person': event['involved_person'], 'gender': event['gender'],
                              'legislation': event['legislation'], 'time': event['datetime'],
                              'street': event['location']['street']['name'], 'type': event['type'],
                              'object of search': event['object_of_search']})

    return relevant_data


'''
if __name__ == "__main__":

    load_dotenv()

    coords = postcode_to_coords(ENV["MY_POSTCODE"])

    jan_crime_data = get_relevant_street_crimes_data(coords, 2023, 1)

    dict_to_csv(jan_crime_data, 'Jan23 Crime Data')

    jan_ss_data = get_relevant_stop_and_search_data(coords, 2023, 1)

    print(len(jan_ss_data))

    dict_to_csv(jan_ss_data, 'Jan23 SS Data')
'''
