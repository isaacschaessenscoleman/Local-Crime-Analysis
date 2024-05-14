'''This file contains all of the functions related to the analysis of the the extracted data
(crime and stop & search (ss) instances).'''

from os import environ as ENV

from dotenv import load_dotenv
import pandas as pd

from .extract import postcode_to_coords, get_relevant_street_crimes_data, get_relevant_stop_and_search_data

crime_categories = ['category', 'street name', 'outcome']
ss_categories = ['age range', 'gender', 'legislation',
                 'object of search', 'street', 'type', 'time', 'hour']


def get_crime_data_df(post_code: str, year: int, month: int) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of crimes."""

    coords = postcode_to_coords(post_code)
    crime_data = get_relevant_street_crimes_data(coords, year, month)

    return pd.DataFrame(crime_data)


def get_ss_data_df(post_code: str, year: int, month: int) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of stop and searches (ss)."""

    coords = postcode_to_coords(post_code)
    ss_data = get_relevant_stop_and_search_data(coords, year, month)
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

    crime_df = get_crime_data_df(ENV['MY_POSTCODE'], 2023, 1)

    ss_df = get_ss_data_df(ENV['MY_POSTCODE'], 2023, 1)

    print(counting_by_category(crime_df, ['street name', 'category']))

    # print(ss_df[['time', 'hour']].head())
