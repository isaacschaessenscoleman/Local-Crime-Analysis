'''This file contains all of the functions that produce visualisations from the extracted data.'''

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use

from .analyse import get_crime_data_df, get_ss_data_df, counting_by_category


def plot_bar(df: pd.core.frame.DataFrame, file_path: str) -> None:
    """This function produces a bar chart based on the inputted dataframe and category for
    the bars. The function saves the image to the inputted filepath."""

    font_dict = {'weight': 'bold', 'size': 14}

    print('4')
    use('agg')
    sns.set_theme(style='darkgrid', palette='deep', font='monospace')
    print('5')
    plt.figure(facecolor='lightgray')
    print('6')
    bar_plot = sns.barplot(y=df.index, x=df[df.columns[0]], orient='h')
    print('7')
    plt.xlabel('Number of Crimes', fontdict=font_dict)
    plt.ylabel('Category', fontdict=font_dict)
    plt.title('Number of Crimes by Category', fontdict=font_dict)

    plt.savefig(file_path, bbox_inches='tight')


'''
if __name__ == "__main__":

    crime_df = get_crime_data_df('NW5 1TU', 2023, 1)

    crime_cat_df = counting_by_category(crime_df, ['outcome'])

    file_path = "static/png/category_chart"

    plot_bar(crime_cat_df, file_path)
'''
