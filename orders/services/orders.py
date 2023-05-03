import json

import requests
from loguru import logger
from rest_framework import status
from orders.models import Orders
from orders.boxberryAPI import BoxberryAPI
from orders.services.notify import NotifyService


class OrdersServices:

    def __init__(self):
        self.boxberry = BoxberryAPI()

    def create_order(self, data: dict) -> dict:

        """
        Функция готовит данные и передает их для создания
        нового отправления в Boxberry

        :param data: Словарь с данными о заказе
        :return : dict
        """

        payload = {
            "order_id": data["order_id"],  # Номер заказа из интернет-магазина
            "price": 5,  # Объявленная стоимость
            "vid": 1,  # Вид доставки: по умолчанию ПВЗ
            "delivery_sum": result["total_cost"],
            "shop": {  # Блок с информацией о пункте приема и пункте выдачи отправления
                "name": data["destination_point"],  # Код пункта выдачи
                "name1": data["departure_point"]  # Код пункта отправки
            },
            "customer": {  # Блок с информацией о получателе отправления
                "fio": data["customer_fio"],
                "phone": data["customer_phone"],
                "email": data["customer_email"]
            },
            "items": data["items"],
            "weights": self._create_shipments(result["boxes"])  # блок с информацией о тарных местах
        }

        response = self.boxberry.send_request_to_create_order(payload)

        if response:
            return response.json()
        return {}

    @staticmethod
    def _create_shipments(boxes: list) -> dict:
        """
        Функция формирует грузоместа для поле weights.
        Возможно максимум 24 места

        :param boxes: Обработанный в Packer список отправлений
        :return: Возвращает словарь weight, weight2 ...

        """
        weights = {}

        for box in boxes:
            weights["weight" + str(box["box"])] = box["weight"]

        weight1 = weights.pop("weight1")
        weights["weight"] = weight1

        return weights

    def check_status_delivery_order(self):
        """
        Функция проверяет статус отправления и
        сохраняет его в таблице бд.

        :param:
        :return: None

        """
        print("Boxberry: check_status_delivery_order: Start")
        orders = Orders.objects.exclude(order_status="Успешно Выдан").exclude(order_status="Заказ возвращен в "
                                                                                           "Интернет-магазин")

        if orders:
            for order in orders:
                response = self.boxberry.get_last_statuses(order.track_number)

                if response:

                    last_status = response.json()[order.track_number]["lastStatusName"]

                    if order.order_status != last_status:
                        order.order_status = last_status
                        order.save()

                        self._send_notify_to_client(last_status, order.order_id)

                        logger.info(f"Boxberry: check_status_delivery_order: Статус отправления"
                                    f" {order.order_id} изменился на {last_status}")

                        return status.HTTP_201_CREATED

    @staticmethod
    def _send_notify_to_client(new_status: str, order_id: str) -> None:
        """
        Функция отправляет уведомление клиенту при поступлении заказа
        в ПВЗ или если клиент забрал заказ.

        :param new_status: Новый статус отправления
        :param order_id: ID заказа из интернет-магазина
        :return: None
        """

        if new_status == "Доступен к получению в Пункте выдачи":
            message = f"Заказ № {order_id} готов к выдаче. Телефон: 88001005441. МК Электро"
            NotifyService().send_email(subject=f"Информация по доставке {order_id}",
                                       message=message)

            # NotifyService().send_sms(message, order.phone)

        elif new_status == "Успешно Выдан":
            message = f"Спасибо за покупку! Будем рады Вашему отзыву: https://mkelektro.ru/rev"
            NotifyService().send_email(subject=f"Информация по доставке {order_id}",
                                       message=message)

            # NotifyService().send_sms(message, order.phone)
