from django.shortcuts import render

# Create your views here.

import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound

from django.core.cache import cache
from django.shortcuts import render


from data.analyse import get_crime_data_df, counting_by_category
from data.visualise import plot_bar, plot_crimes_with_time_line_graph
# from ..data.analyse import get_crime_data_df, counting_by_category
# from ..data.visualise import plot_bar, plot_crimes_with_time_line_graph

from datetime import datetime

# Create your views here.


def home(request):
    return HttpResponse(f"Hello, world. You're at the stop and search home page.\n {request.body}\n{request.path}")


def postcode_page(request, postcode):

    return HttpResponse("Stop and search stats for %s" % postcode)
