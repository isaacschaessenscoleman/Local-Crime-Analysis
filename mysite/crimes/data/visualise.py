'''This file contains all of the functions that produce visualisations from the extracted data.'''

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use

from .analyse import get_ss_data_df, counting_by_category, get_crime_data_df


def plot_bar(df: pd.core.frame.DataFrame, file_path: str) -> None:
    """This function produces a bar chart based on the inputted dataframe and category for
    the bars. The function saves the image to the inputted filepath."""

    font_dict = {'weight': 'bold', 'size': 14}

    use('agg')
    sns.set_theme(style='darkgrid', palette='deep', font='monospace')
    plt.figure(facecolor='lightgray')
    sns.barplot(y=df.index, x=df[df.columns[0]], orient='h')
    plt.xlabel('Number of Crimes', fontdict=font_dict)
    plt.ylabel(df.columns[0].title(), fontdict=font_dict)
    plt.title(
        f'Number of Crimes by {df.columns[0].title()}', fontdict=font_dict)
    plt.savefig(file_path, bbox_inches='tight')


def plot_crimes_with_time_line_graph(df: pd.core.frame.DataFrame, file_path: str) -> None:
    """This function produces a line graph based on the inputted dataframe
    with two columns: date and total number of crimes (the inputted dataframe may 
    be filtered in some way - e.g. specific street(s) or category of crime).
    The function saves an image of the graph to the inputted filepath."""

    font_dict = {'weight': 'bold', 'size': 14}

    use('agg')
    sns.set_theme(style='darkgrid', palette='deep', font='monospace')
    plt.figure(facecolor='lightgray')
    sns.lineplot(x=df.index, y=df[df.columns[0]],
                 marker='.', markersize=10, markerfacecolor='gray')
    plt.xlabel('Date (Month-Year)', fontdict=font_dict)
    plt.xticks(ticks=df.index, labels=[
               date.strftime("%m-%Y") for date in df.index], rotation=305)
    plt.ylabel('Number of Crimes', fontdict=font_dict)
    plt.title(
        f'Number of Crimes by {df.columns[0].title()}', fontdict=font_dict)
    plt.savefig(file_path, bbox_inches='tight')


'''
if __name__ == "__main__":

    # crime_df = get_crime_data_df('NW5 1TU', 2023, 1)

    # crime_cat_df = counting_by_category(crime_df, ['outcome'])

    all_crime_df = get_crime_data_df('nw5 1tu', 2023)
    all_crime_date_df = counting_by_category(all_crime_df, ['date'])

    print(all_crime_date_df)

    plot_crimes_with_time_line_graph(all_crime_date_df, 'yo')
'''
