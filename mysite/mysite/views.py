import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.http import HttpResponseNotFound

from django.core.cache import cache
from django.shortcuts import render

from datetime import datetime

# Create your views here.


def home(request):
    return HttpResponse(f"THIS IS THE HOME PAGE\n {request.body}\n{request.path}")
