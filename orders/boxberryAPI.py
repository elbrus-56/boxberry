from typing import Optional
import requests
from django.conf import settings
from requests import Response
from loguru import logger

logger.add("orders.log")


class BoxberryAPI:
    def __init__(self):
        self.url = "https://api.boxberry.ru/json.php"
        self.token = settings.BOXBERRY_TOKEN

    def post_api(self, data: dict) -> Optional[Response]:
        """
        Функция отправляет запрос к API Boxberry

        :param data: Принимает словарь с информацией о методе API и его параметрами
        :return: :class:`Response <Response>` object or None

        """
        data.update(token=self.token)

        try:
            r = requests.post(self.url, json=data)
        except Exception as e:
            logger.error(f"Boxberry: post_api: Сайт {self.url} недоступен, ошибка соединения с {data} - {e}")
            return
        else:
            if "err" not in r.json():
                return r
            else:
                logger.error(f"Boxberry: post_api: {r.json()} with {data}")
                return

    def send_request_to_create_order(self, data: dict) -> Optional[Response]:
        """
          Функция выполняет метод ParselCreate для
          создания нового отправления

          :param data: Словарь с информацией о заказе
          :return: :class:`Response <Response>` object or None

          """

        payload = {
            "method": "ParselCreate",
            "sdata": data
        }

        return self.post_api(payload)

    def get_last_statuses(self, track_number: str) -> Optional[Response]:
        """
          Функция выполняет метод GetLastStatusData для
          получения последнего статуса отправления

          :param track_number:
          :return: :class:`Response <Response>` object or None

        """

        payload = {
            "method": "GetLastStatusData",
            "trackNumbers": [track_number]
        }
        return self.post_api(payload)
