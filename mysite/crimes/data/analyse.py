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

crime_categories = ['category', 'street name', 'outcome']
ss_categories = ['age range', 'gender', 'legislation',
                 'object of search', 'street', 'type', 'time', 'hour']


def get_crime_data_df(post_code: str) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of crimes."""

    coords = postcode_to_coords(post_code)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    start = time.time()

    dates = []
    for year in range(2022, current_year+1):
        if year == current_year:
            dates += [(coords, year, i) for i in range(1, current_month-1)]
        else:
            dates += [(coords, year, i) for i in range(1, 13)]

    dates_list = time.time()

    crime_data = []
    for date in dates:
        c = time.time()
        crime_data += get_relevant_street_crimes_data(
            coords, date[1], date[2])
        print(time.time()-c)

    no_multi_p = time.time()

    crime_dataa = []
    with Pool() as pool:
        api_limit = 15
        beginning_of_for_loop = time.time()
        for i in range(0, len(dates), api_limit):
            pp = time.time()
            crime_dataa += pool.starmap(
                get_relevant_street_crimes_data, dates[i:i+api_limit])
            time.sleep(1)

            print(time.time() - pp)
        end_of_for_loop = time.time()

    aa = time.time()
    crime_dataa = [crime for sublist in crime_dataa for crime in sublist]
    bb = time.time()
    multi_p = time.time()

    print(
        f"Date:{dates_list-start}\nNo multi: {no_multi_p-dates_list}\nmulti: {multi_p-no_multi_p}")

    print(end_of_for_loop - beginning_of_for_loop)
    print(bb-aa)

    return pd.DataFrame(crime_data)


def get_ss_data_df(post_code: str) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of stop and searches (ss)."""

    coords = postcode_to_coords(post_code)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    dates = []
    for year in range(2022, current_year+1):
        if year == current_year:
            dates += [(i, year) for i in range(1, current_month-1)]
        else:
            dates += [(i, year) for i in range(1, 13)]

    ss_data = []
    for date in dates:
        ss_data += get_relevant_stop_and_search_data(
            coords, date[1], date[0])

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

    print(os.cpu_count())

    # crime_df = get_crime_data_df(ENV['MY_POSTCODE'], 2023, 1)

    # ss_df = get_ss_data_df(ENV['MY_POSTCODE'], 2023, 1)

    # print(counting_by_category(crime_df, ['street', 'category']))

    # print(ss_df[['time', 'hour']].head())

    df = get_crime_data_df('NW51TU')

    print(df.head())

    print(df.shape)

    # ss_df = get_ss_data_df('nw5 1tu')

    # print(ss_df.head())

    # print(ss_df.shape)

    # print(ss_df['date'].unique())
