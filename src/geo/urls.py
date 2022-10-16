from django.urls import path

from .views import get_cities, get_countries, get_weather

urlpatterns = [
    path("city/<str:name>", get_cities, name="city"),
    path("country/<str:name>", get_countries, name="country"),
    path("weather/<str:alpha2code>/<str:city>", get_weather, name="weather"),
]
