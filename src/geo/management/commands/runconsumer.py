from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from app.settings import RABBITMQ_URI
from geo.management.commands._consumer import EventConsumer


class Command(BaseCommand):
    """
    Реализация функций консольной команды.

    https://docs.djangoproject.com/en/4.1/howto/custom-management-commands
    """

    help = "Обработка очереди поступающих событий."

    argument_queue: str = "queue"

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Добавление аргументов для команды.

        :param parser: Объект парсера консольной команды.
        :return:
        """

        parser.add_argument(
            self.argument_queue,
            type=str,
            help="Название очереди",
        )

    def handle(self, *args: tuple, **options: dict[str, Any]) -> None:
        """
        Выполнение консольной команды.
        https://docs.python.org/3/library/argparse.html#example

        :param args: Позиционные аргументы консольной команды.
        :param options: Опции консольной команды.
        :return:
        """

        # инициализация и запуск консьюмера
        EventConsumer(
            url=RABBITMQ_URI,
            queue_name=str(options.get(self.argument_queue, "default")),
        )
