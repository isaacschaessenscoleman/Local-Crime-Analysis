import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound

from django.core.cache import cache
from django.shortcuts import render

from .data.analyse import get_crime_data_df, counting_by_category
from .data.visualise import plot_bar, plot_crimes_with_time_line_graph

from datetime import datetime

# Create your views here.


def home(request):
    return HttpResponse(f"Hello, world. You're at the crime home page.\n {request.body}\n{request.path}")


def postcode_page(request, postcode):

    print(datetime.today().strftime('%Y-%m-%d'))

    if request.method == 'POST':
        return HttpResponse('post request received - from: %s to: %s' % (request.POST.get('from-date'), request.POST.get('to-date')))

    if request.method == 'GET':

        crime_df_dict = cache.get('cached_crime_df_dict')

        if (crime_df_dict is None):

            try:
                crime_df = get_crime_data_df(postcode, 2022)
                crime_df_dict = {postcode: crime_df}
                cache.set('cached_crime_df_dict',
                          crime_df_dict, timeout=60 * 10)
            except Exception as e:
                # Print out the error message
                print(f"An error occurred: {e}")
                return HttpResponseNotFound(f"{e} Error\n\nIf it's a 429 error just try refreshing again :)))))")

        if postcode not in crime_df_dict.keys():

            try:
                crime_df = get_crime_data_df(postcode, 2022)
                crime_df_dict = cache.get('cached_crime_df_dict')
                crime_df_dict[postcode] = crime_df
                cache.set('cached_crime_df_dict',
                          crime_df_dict, timeout=60 * 10)
            except Exception as e:
                # Print out the error message
                print(f"An error occurred: {e}")
                return HttpResponseNotFound(f"{e} Error\n\nIf it's a 429 error just try refreshing again :)))))")

        crime_df = crime_df_dict[postcode]

        # Line Graph
        crime_date_df = counting_by_category(crime_df, ['date'])
        plot_crimes_with_time_line_graph(
            crime_date_df, "crimes/static/png/line_graph")

        # Category Bar Chart
        crime_category_df = counting_by_category(crime_df, ['category'])
        plot_bar(crime_category_df, "crimes/static/png/bar_chart")

        # Streets Table
        crime_street_df = crime_df.groupby('street')['category'].agg(
            lambda x: x.mode().iloc[0] if not x.empty else None).reset_index()
        crime_street_df['total_crimes'] = crime_df.groupby(
            'street').size().reset_index(name='total_crimes')['total_crimes']

        context = {"postcode": postcode[:-3].strip().upper() + ' ' + postcode[-3:].strip().upper(),
                   "crime_street_df": crime_street_df.sort_values('total_crimes', ascending=False).head(10).iterrows(),
                   "today": datetime.today().strftime('%Y-%m-%d')}

        return render(request, "crimes/postcode_page.html", context)
