'''This file contains all of the functions related to the analysis of the the extracted data
(crime and stop & search (ss) instances).'''

from datetime import datetime
from multiprocessing.pool import Pool
from os import environ as ENV
import os
import time

from dotenv import load_dotenv
import pandas as pd

from .extract import postcode_to_coords, get_relevant_street_crimes_data, get_relevant_stop_and_search_data

crime_categories = ['category', 'street name', 'outcome', 'date']
ss_categories = ['age range', 'gender', 'legislation',
                 'object of search', 'street', 'type', 'time', 'hour', 'date']


def get_crime_data_df(post_code: str, starting_year: int) -> pd.core.frame.DataFrame:
    """Given a postcode and a starting year, this function returns a pandas
    dataframe with data on instances of crimes from that year."""

    coords = postcode_to_coords(post_code)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    dates = []
    for year in range(starting_year, current_year+1):
        if year == current_year:
            dates += [(coords, year, i) for i in range(1, current_month-1)]
        else:
            dates += [(coords, year, i) for i in range(1, 13)]

    crime_data = []
    with Pool() as pool:
        api_limit = 15
        for i in range(0, len(dates), api_limit):

            crime_data += pool.starmap(
                get_relevant_street_crimes_data, dates[i:i+api_limit])
            time.sleep(1)

    crime_data = [crime for sublist in crime_data for crime in sublist]

    return pd.DataFrame(crime_data)


def get_ss_data_df(post_code: str, starting_year: int) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of stop and searches (ss)."""

    coords = postcode_to_coords(post_code)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    dates = []
    for year in range(starting_year, current_year+1):
        if year == current_year:
            dates += [(coords, year, i) for i in range(1, current_month-1)]
        else:
            dates += [(coords, year, i) for i in range(1, 13)]

    ss_data = []
    with Pool() as pool:
        api_limit = 15

        for i in range(0, len(dates), api_limit):
            ss_data += pool.starmap(
                get_relevant_stop_and_search_data, dates[i:i+api_limit])
            time.sleep(1)

    ss_data = [ss for sublist in ss_data for ss in sublist]
    ss_df = pd.DataFrame(ss_data)
    ss_df['time'] = ss_df['time'].apply(lambda x: x[11:-9])
    ss_df['hour'] = ss_df['time'].str[:2]

    return ss_df


def counting_by_category(df: pd.core.frame.DataFrame, categories: list[str]) -> pd.core.frame.DataFrame:
    """Given a pandas dataframe, this function returns a dataframe with
    the number of rows (counts) for each type of the inputted category(ies).
    Note: This function is designed to deal with our specific data sources 
    (i.e. crime and stop&search data)."""

    for category in categories:
        if category.lower() not in crime_categories+ss_categories:
            raise ValueError(
                f" {category} is not a valid category that you can search this data by.")

    return df.groupby(categories)[categories].count()


if __name__ == "__main__":

    load_dotenv()

    ss_df = get_ss_data_df('nw5 1tu', 2022)

    print(ss_df.head())

    print(ss_df.shape)

    # print(ss_df['date'].unique())
