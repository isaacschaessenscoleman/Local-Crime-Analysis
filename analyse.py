'''This file contains all of the functions related to the analysis of the the extracted data.'''

from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv

from extract import postcode_to_coords, get_relevant_street_crimes_data, get_relevant_stop_and_search_data


def get_crime_data_df(post_code: str, year: int, month: int) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of crimes."""

    coords = postcode_to_coords(post_code)
    crime_data = get_relevant_street_crimes_data(coords, year, month)

    return pd.DataFrame(crime_data)


def crimes_per_category(crime_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas series of the number of crimes per
    category."""

    return crime_df.groupby('category')['category'].count()


def crimes_per_street(crime_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas series of the number of crimes per
    street."""

    return crime_df.groupby('street name')['street name'].count().sort_values(ascending=False)


def crimes_per_outcome(crime_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas series of the number of crimes for
    each outcome."""

    return crime_df.groupby('outcome')['outcome'].count().sort_values(ascending=False)


def crimes_per_outcome_per_category(crime_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas series of the number of crimes for
    each outcome per category."""

    return crime_df.groupby(['category', 'outcome'])['outcome'].count()


def crimes_per_outcome_per_category_per_street(crime_df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas dataframe of the number of crimes for
    each outcome per category per street."""

    return crime_df.groupby(['street name', 'category', 'outcome']).count()


def crimes_per_outcome_per_category_for_specific_street(crime_df: pd.core.frame.DataFrame, street_name: str) -> pd.core.frame.DataFrame:
    """Given a dataframe related to crime events in a certain area, during a certain
    time period, this function returns a pandas dataframe of the number of crimes for
    each outcome per a specified street."""

    return crime_df[crime_df['street name'].str.contains(street_name, case=False)].groupby(['category', 'outcome']).count()


def get_ss_data_df(post_code: str, year: int, month: int) -> pd.core.frame.DataFrame:
    """Given a postcode, year and month, this function returns a pandas
    dataframe with data on instances of stop and searches."""

    coords = postcode_to_coords(post_code)
    ss_data = get_relevant_stop_and_search_data(coords, year, month)

    return pd.DataFrame(ss_data)


def ss_per_age_range(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per age category."""

    return ss_df.groupby('age range')['age range'].count()


def ss_per_gender(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per gender."""

    return ss_df.groupby('gender')['gender'].count()


def ss_per_legislation(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per type of legislation."""

    return ss_df.groupby('legislation')['legislation'].count()


def ss_per_object_of_search(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per type of 'object of search'."""

    return ss_df.groupby('object of search')['object of search'].count()


def ss_per_street(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per street."""

    return ss_df.groupby('street')['street'].count().sort_values(ascending=False)


def ss_per_type(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per stop and search type."""

    return ss_df.groupby('type')['type'].count()


def ss_per_hour(ss_df: pd.core.frame.DataFrame) -> pd.core.series.Series:
    """Given a dataframe related to stop and search events in a certain area, during
    a certain time period, this function returns a pandas series of the number of stop
    and searches per hour of the day."""

    return ss_df.groupby(ss_df['time'].str[:2]).size()


if __name__ == "__main__":

    load_dotenv()

    crime_df = get_crime_data_df(ENV['MY_POSTCODE'], 2023, 1)

    ss_df = get_ss_data_df(ENV['MY_POSTCODE'], 2023, 1)

    a = crimes_per_category(crime_df)

    print(type(a))

    # NOTE: A LOT OF THESE FUNCTIONS HAVE A VERY SIMILAR FORM ... THERE'S PROBABLY POTENTIAL FOR REFACTORING
