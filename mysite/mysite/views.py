import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token

from django.core.cache import cache
from django.shortcuts import render, redirect

from datetime import datetime

from crimes.views import postcode_page as crime_post_code_page
from stop_and_searches.views import postcode_page as ss_postcode_page

# Create your views here.


def home(request):
    context = {}

    return render(request, "mysite/home_page.html", context)


def search_queries(request):
    context = {}

    if request.method == 'POST':

        postcode = request.POST.get('postcode')
        page = request.POST.get('webpage')

        if page == 'Crimes':
            return redirect(f'crimes/{postcode}')

        if page == "Stop and Searches":
            return redirect(f'stop_and_searches/{postcode}')
