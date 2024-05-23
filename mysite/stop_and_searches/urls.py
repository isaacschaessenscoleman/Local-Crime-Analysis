from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("<str:postcode>/", views.postcode_page, name="postcode__page"),
]
