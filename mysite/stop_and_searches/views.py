from django.shortcuts import render

# Create your views here.

import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound

from django.core.cache import cache
from django.shortcuts import render


from data.analyse import get_ss_data_df, counting_by_category
from data.visualise import plot_bar, plot_crimes_with_time_line_graph, object_of_search_bar_chart, stop_and_search_pie_chart


from datetime import datetime

# Create your views here.


def home(request):
    return HttpResponse(f"Hello, world. You're at the stop and search home page.\n {request.body}\n{request.path}")


def postcode_page(request, postcode):

    normal_postcode = postcode.replace(" ", "").lower()
    print('hello')

    if request.method == 'GET':

        print('GET REQUEST')

        ss_df_dict = cache.get('cached_ss_df_dict')
        print(f"S&S Dict Data: {ss_df_dict}")
        print('hellooooooo')

        if (ss_df_dict is None):

            print('NO CACHED DICTIONARY WITH SS DATAFRAMES')

            try:
                ss_df = get_ss_data_df(normal_postcode, 2022)
                print('DATAFRAME CREATED')
                ss_df_dict = {normal_postcode: ss_df}
                cache.set('cached_ss_df_dict',
                          ss_df_dict, timeout=60 * 10)
            except Exception as e:
                # Print out the error message
                print(f"An error occurred: {e}")
                return HttpResponseNotFound(f"{e} Error\n\nIf it's a 429 error just try refreshing again :)))))")

        elif normal_postcode not in ss_df_dict.keys():

            try:
                ss_df = get_ss_data_df(normal_postcode, 2022)
                ss_df_dict[normal_postcode] = ss_df
                cache.set('cached_ss_df_dict',
                          ss_df_dict, timeout=60 * 10)
            except Exception as e:
                # Print out the error message
                print(f"An error occurred: {e}")
                return HttpResponseNotFound(f"{e} Error\n\nIf it's a 429 error just try refreshing again :)))))")

        print('GET METHOD')
        print(f"postcode: {normal_postcode}")
        print(ss_df_dict.keys())
        print([type(value) for value in ss_df_dict.values()])
        ss_df = ss_df_dict[normal_postcode]

        # CREATING GRAPHS, TO SAVE AND THEN IMPLEMENT INTO HTML PAGE
        '''
        # Line Graph
        crime_date_df = counting_by_category(crime_df, ['date'])
        plot_crimes_with_time_line_graph(
            crime_date_df, "crimes/static/png/line_graph")

        # Category Bar Chart
        crime_category_df = counting_by_category(crime_df, ['category'])
        plot_bar(crime_category_df, "crimes/static/png/bar_chart")
        

        # Streets Table
        ss_street_df = ss_df.groupby('street')['category'].agg(
            lambda x: x.mode().iloc[0] if not x.empty else None).reset_index()
        ss_street_df['total_ss'] = ss_df.groupby(
            'street').size().reset_index(name='total_ss')['total_ss']
            '''

        context = {"postcode": normal_postcode[:-3].strip().upper() + ' ' + normal_postcode[-3:].strip().upper(),
                   "starting_date": "2022-01-01",
                   "ending_date": datetime.today().strftime('%Y-%m-%d')}

        return render(request, "stop_and_searches/ss_postcode_page.html", context)

    if request.method == 'POST':

        from_date = datetime.strptime(
            request.POST.get('from-date'), "%Y-%m-%d")
        to_date = datetime.strptime(
            request.POST.get('to-date'), "%Y-%m-%d")

        ss_df_dict = cache.get('cached_ss_df_dict')

        print('GET METHOD')
        print(f"postcode: {normal_postcode}")
        print(ss_df_dict.keys())

        ss_df = ss_df_dict[normal_postcode]

        print(ss_df['date'])
        print(from_date)

        ss_df = ss_df[(ss_df.date >= from_date)
                      & (ss_df.date <= to_date)]

        #  CREATING GRAPHS, TO SAVE AND THEN IMPLEMENT INTO HTML PAGE

        '''
        # Line Graph
        ss_date_df = counting_by_category(ss_df, ['date'])
        plot_crimes_with_time_line_graph(
            ss_date_df, "stop_and_searches/static/png/line_graph")

        # Category Bar Chart
        crime_category_df = counting_by_category(crime_df, ['category'])
        plot_bar(crime_category_df, "crimes/static/png/bar_chart")
        '''

        # Streets Table
        ss_street_df = ss_df.groupby('street')['category'].agg(
            lambda x: x.mode().iloc[0] if not x.empty else None).reset_index()
        ss_street_df['total_ss'] = ss_df.groupby(
            'street').size().reset_index(name='total_ss')['total_ss']

        context = {"postcode": normal_postcode[:-3].strip().upper() + ' ' + normal_postcode[-3:].strip().upper(),
                   "ss_street_df": ss_street_df.sort_values('total_ss', ascending=False).head(10).iterrows(),
                   "starting_date": str(from_date.date()),
                   "ending_date": str(to_date.date())}

        return render(request, "stop_and_searches/ss_postcode_page.html", context)
