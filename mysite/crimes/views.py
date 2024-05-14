import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound


from django.shortcuts import render
from django.template import loader

from .data.analyse import get_crime_data_df, counting_by_category
from .data.visualise import plot_bar

# Create your views here.


def home(request):
    return HttpResponse(f"Hello, world. You're at the crime home page.\n {request.body}\n{request.path}")


def postcode_page(request, postcode):
    '''
    crime_df = get_crime_data_df("%s" % postcode, 2023, 1)
    street_data = counting_by_category(crime_df, ["street name"])
    '''

    try:
        crime_df = get_crime_data_df(postcode, 2023, 1)
    except:
        return HttpResponseNotFound("404 Error: Invalid Postcode")

    crime_category_df = counting_by_category(crime_df, ['category'])
    plot_bar(crime_category_df, f"crimes/static/png/bar_chart")

    crime_street_df = crime_df.groupby('street')['category'].agg(
        lambda x: x.mode().iloc[0] if not x.empty else None).reset_index()
    crime_street_df['total_crimes'] = crime_df.groupby(
        'street').size().reset_index(name='total_crimes')['total_crimes']

    context = {"postcode": postcode.upper(),
               "crime_street_df": crime_street_df.sort_values('total_crimes', ascending=False).head(10).iterrows()}

    return render(request, "crimes/postcode_page.html", context)
