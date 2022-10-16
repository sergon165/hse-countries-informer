"""Представления Django"""
from typing import Any

from django.core.cache import caches
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from app.settings import CACHE_WEATHER
from geo.serializers import CountrySerializer, CitySerializer
from geo.services.city import CityService
from geo.services.country import CountryService
from geo.services.weather import WeatherService


@api_view(["GET"])
def get_cities(request: Request, name: str) -> JsonResponse:
    """
    Получить информацию о городах по названию.
    Сначала метод ищет данные в БД. Если данные не найдены, то делается запрос к API.
    После получения данных от API они сохраняются в БД.

    :param Request request: Объект запроса
    :param str name: Название города
    :return:
    """

    if cities := CityService().get_cities(name):
        serializer = CitySerializer(cities, many=True)

        return JsonResponse(serializer.data, safe=False)

    raise NotFound


@api_view(["GET"])
def get_countries(request: Request, name: str) -> JsonResponse:
    """
    Получение информации о странах по названию.
    Сначала метод ищет данные в БД. Если данные не найдены, то делается запрос к API.
    После получения данных от API они сохраняются в БД.

    :param Request request: Объект запроса
    :param str name: Название страны
    :return:
    """

    if countries := CountryService().get_countries(name):
        serializer = CountrySerializer(countries, many=True)

        return JsonResponse(serializer.data, safe=False)

    raise NotFound


@api_view(["GET"])
def get_weather(request: Request, alpha2code: str, city: str) -> JsonResponse:
    """
    Получение информации о погоде в указанном городе.

    :param Request request: Объект запроса
    :param str alpha2code: ISO Alpha2 код страны
    :param str city: Город
    :return:
    """

    cache_key = f"{alpha2code}_{city}"
    data = caches[CACHE_WEATHER].get(cache_key)
    if not data:
        if data := WeatherService().get_weather(alpha2code=alpha2code, city=city):
            caches[CACHE_WEATHER].set(cache_key, data)

    if data:
        return JsonResponse(data)

    raise NotFound


@api_view(["GET"])
def get_currency(*args: Any, **kwargs: Any) -> None:
    pass
