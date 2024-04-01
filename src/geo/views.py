"""Представления Django"""
import re
from typing import Any

from django.core.cache import caches
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.settings import api_settings

from app.settings import CACHE_WEATHER, CACHE_CURRENCY
from geo.serializers import (
    CountrySerializer,
    CitySerializer,
    WeatherSerializer,
    CurrencySerializer,
)
from geo.services.city import CityService
from geo.services.country import CountryService
from geo.services.currency import CurrencyService
from geo.services.shemas import CountryCityDTO
from geo.services.weather import WeatherService


@api_view(["GET"])
def get_city(request: Request, name: str) -> JsonResponse:
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
def get_cities(request: Request) -> JsonResponse:
    """
    Получение информации о городах с фильтрацией по ISO Alpha2 коду страны и названию города.

    :param Request request: Объект запроса
    :return:
    """

    codes_set = set()
    if codes := request.query_params.getlist("codes"):
        if any(not re.match(r"\w{2},\w{2,50}", code) for code in codes):
            raise ValidationError({"codes": "Коды переданы в некорректном формате."})

        codes_set = {
            CountryCityDTO(alpha2code=alpha2code, city=city)
            for (alpha2code, city) in (code.split(",") for code in codes)
        }

    if not codes_set:
        raise ValidationError(
            {
                "codes": "Не переданы ISO Alpha2 коды стран и названия городов для поиска."
            }
        )

    if cities := CityService().get_cities_by_codes(codes_set):
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        page = paginator.paginate_queryset(cities, request)
        serializer = CitySerializer(page, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse([], safe=False)


@api_view(["GET"])
def get_country(request: Request, name: str) -> JsonResponse:
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
def get_countries(request: Request) -> JsonResponse:
    """
    Получение информации о странах с фильтрацией по их ISO Alpha2 коду страны.

    :param Request request: Объект запроса
    :return:
    """

    codes_set = set()
    if codes := request.query_params.getlist("codes"):
        codes_set = {code.strip() for code in codes if code.strip().isalpha()}

    if not codes_set:
        raise ValidationError(
            {"codes": "Не переданы ISO Alpha2 коды стран для поиска."}
        )

    if countries := CountryService().get_countries_by_codes(codes_set):
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        page = paginator.paginate_queryset(countries, request)
        serializer = CountrySerializer(page, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse([], safe=False)


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
        serializer = WeatherSerializer(data)
        return JsonResponse(serializer.data)

    raise NotFound


@api_view(["GET"])
def get_currency(request: Request, base: str) -> JsonResponse:
    """
    Получение информации о курсах валют.

    :param Request request: Объект запроса
    :param str base: Базовая валюта
    :return:
    """

    cache_key = f"{base}"
    data = caches[CACHE_CURRENCY].get(cache_key)
    if not data:
        if data := CurrencyService().get_currency(base=base):
            caches[CACHE_CURRENCY].set(cache_key, data)

    if data:
        serializer = CurrencySerializer(data)
        return JsonResponse(serializer.data)

    raise NotFound
