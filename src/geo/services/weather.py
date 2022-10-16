from typing import Optional

from geo.clients.shemas import CountryDTO
from geo.clients.weather import WeatherClient
from geo.models import Country


class WeatherService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_weather(self, alpha2code: str, city: str) -> Optional[dict]:
        """
        Получение списка стран по названию.

        :param alpha2code: ISO Alpha2 код страны
        :param city: Город
        :return:
        """

        if data := WeatherClient().get_weather(f"{city},{alpha2code}"):
            return data

        return None

    def build_model(self, country: CountryDTO) -> Country:
        """
        Формирование объекта модели страны.

        :param CountryDTO country: Данные о стране.
        :return:
        """

        return Country(
            alpha3code=country.alpha3code,
            name=country.name,
            alpha2code=country.alpha2code,
            capital=country.capital,
            region=country.region,
            subregion=country.subregion,
            population=country.population,
            latitude=country.latitude,
            longitude=country.longitude,
            demonym=country.demonym,
            area=country.area,
            numeric_code=country.numeric_code,
            flag=country.flag,
            currencies=[currency.code for currency in country.currencies],
            languages=[language.name for language in country.languages],
        )
