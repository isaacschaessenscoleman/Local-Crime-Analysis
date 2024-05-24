'''This file contains all of the functions that produce visualisations from the extracted data.'''

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use
from matplotlib.colors import ListedColormap

from .analyse import get_ss_data_df, counting_by_category, get_crime_data_df


def plot_bar(df: pd.core.frame.DataFrame, file_path: str) -> None:
    """This function produces a bar chart based on the inputted dataframe and category for
    the bars. The function saves the image to the inputted filepath."""

    font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}

    use('agg')
    sns.set_theme(style='darkgrid', palette='deep',
                  font='monospace')
    fig = plt.figure(facecolor='#222629')
    ax = fig.add_subplot()
    ax.set_facecolor('#273744')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
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

    font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}

    use('agg')
    sns.set_theme(palette='deep', font='monospace',)
    fig = plt.figure(facecolor='#222629')
    ax = fig.add_subplot()
    ax.set_facecolor('#273744')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    sns.lineplot(x=df.index, y=df[df.columns[0]],
                 marker='.', markersize=10, markerfacecolor='gray')
    plt.xlabel('Date (Month-Year)', fontdict=font_dict)
    plt.xticks(ticks=df.index, labels=[
               date.strftime("%m-%Y") for date in df.index], rotation=305)
    plt.ylabel('Number of Crimes', fontdict=font_dict)
    plt.title(
        f'Number of Crimes by {df.columns[0].title()}', fontdict=font_dict)
    plt.savefig(file_path, bbox_inches='tight')


def object_of_search_bar_chart(df: pd.core.frame.DataFrame, file_path: str, third_var=None):
    """This function produces a horizontal bar chart of the number of stop and
        searches with respect to the object of search. There is also an optional
        argument to add a third variable (age, gender or outcome), creating a
        stacked bar chart."""

    use('agg')

    if third_var is None:

        grouped_df = df.groupby(
            ['object of search']).size()

        font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}
        sns.set_theme(palette='deep', font='monospace')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('#273744')
        fig.patch.set_facecolor('#222629')
        grouped_df.plot(kind='barh', ax=ax,
                        figsize=(10, 6))
        plt.ylabel('Object of Search', fontdict=font_dict)
        plt.xlabel('Number of Searches', fontdict=font_dict)
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        plt.title(f'Number of Stop and Searches by Object of Search',
                  fontdict=font_dict)
        plt.tight_layout()
        plt.savefig(file_path, bbox_inches='tight')

    elif third_var in ["age range", "gender", "outcome"]:

        df = df.groupby(
            ['object of search', third_var]).size().unstack(fill_value=0)

        font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}
        sns.set_theme(palette='deep', font='monospace')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('#273744')
        fig.patch.set_facecolor('#222629')
        df.plot(kind='barh', stacked=True, ax=ax,
                figsize=(10, 6), colormap='Blues')
        plt.ylabel('Object of Search', fontdict=font_dict)
        plt.xlabel('Number of Searches', fontdict=font_dict)
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        plt.title(f'Number of Stop and Searches by Object of Search and {third_var.title()}',
                  fontdict=font_dict)
        plt.legend(title=third_var.title())
        plt.tight_layout()
        plt.savefig(file_path, bbox_inches='tight')

    else:
        raise ValueError(
            "The only valid third variables are 'age range', 'gender' or 'outcome'.")


def stop_and_search_pie_chart(df: pd.core.frame.DataFrame, category: str, loc: str, file_path: str):
    """This function produces a pie chart with the number of stop and searches
    based on a particular category (e.g. 'age range', 'legislation', etc)."""

    use('agg')
    grouped_df = counting_by_category(df, [category])

    font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}
    fig = plt.figure(facecolor='#222629')
    colour_palette = sns.color_palette("ch:s=.25,rot=-.25")
    plt.pie(grouped_df[category],
            colors=colour_palette, autopct='%.0f%%')  # Create pie chart
    fig.legend(grouped_df.index, loc=loc)
    plt.title(
        f'Stop and Searches by {category.title()}', fontdict=font_dict)
    plt.savefig(file_path, bbox_inches='tight')


'''
if __name__ == "__main__":

    # crime_df = get_crime_data_df('NW5 1TU', 2023, 1)

    # crime_cat_df = counting_by_category(crime_df, ['outcome'])

    all_ss_df = get_ss_data_df('nw5 1tu', 2023)

    # STOP AND SEARCH BAR CHART BY HOUR IN THE DAY

    df = counting_by_category(all_ss_df, ['hour'])

    font_dict = {'weight': 'bold', 'size': 12,  'color': 'black'}
    sns.set_theme(palette='deep', font='monospace')
    fig = plt.figure(facecolor='#222629')
    ax = fig.add_subplot()
    ax.set_facecolor('#273744')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    sns.barplot(x=df.index, y=df[df.columns[0]])
    plt.ylabel('Number of Stop and Searches', fontdict=font_dict)
    plt.xlabel(df.columns[0].title(), fontdict=font_dict)
    plt.title("Stop and Searches by Hour", fontdict=font_dict)

    plt.show()
    

    
    # object of search bar chart
    object_of_search_bar_chart(all_ss_df)

    # object of search bar chart by age range
    object_of_search_bar_chart(all_ss_df, 'age range')

    # object of search bar chart by gender
    object_of_search_bar_chart(all_ss_df, 'gender')

    # object of search bar chart by outcome
    object_of_search_bar_chart(all_ss_df, 'outcome')

    # stop and search pie chart by age
    stop_and_search_pie_chart(all_ss_df, 'age range', 'center right')

    # stop and search pie chart by legislation
    stop_and_search_pie_chart(all_ss_df, 'legislation', 'lower center')
'''
