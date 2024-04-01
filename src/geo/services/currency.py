from typing import Optional

from geo.clients.shemas import CurrencyRatesDTO
from geo.clients.currency import CurrencyClient
from geo.models import Country


class CurrencyService:
    """
    Сервис для работы с данными о курсах валют.
    """

    def get_currency(self, base: str) -> Optional[CurrencyRatesDTO]:
        """
        Получение курса валюты.

        :param base: Базовая валюта
        :return:
        """

        if data := CurrencyClient().get_rates(base):
            currency = CurrencyRatesDTO(
                base=data["base"],
                date=data["date"],
                rates=data["rates"]
            )
            return currency

        return None
