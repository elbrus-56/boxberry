import os
from collections import OrderedDict
from unittest import mock

import requests
from django.test import SimpleTestCase, TestCase
# from unittest import TestCase
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from orders.models import Orders, Products
from orders.services.orders import OrdersServices

test_data = {
    "order_id": f"Тестовый заказ {random.randrange(1000000, 100000000)}",
    "destination_point": "5697",
    "departure_point": "74070",
    "customer_fio": "Иванов Иван Иванович",
    "customer_phone": "79998887766",
    "customer_email": "elelel@ssss.ru",
    "items": [
        {
            "id": "U2500220",
            "name": "jjjjj",
            "quantity": 5,
            "price": 1000,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365
        },
        {
            "id": "U2500221",
            "name": "j565656",
            "quantity": 3,
            "price": 100,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365
        }
    ]
}

invalid_data = {
    "order_id": f"Тестовый заказ {random.randrange(1000000, 100000000)}",
    "destination_point": "",
    "departure_point": "74070",
    "customer_fio": "Иванов Иван Иванович",
    "customer_phone": "79998887766",
    "customer_email": "elelel@ssss.ru",
    "items": [
        {
            "id": "U2500220",
            "name": "jjjjj",
            "quantity": 5,
            "price": 1000,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365
        },
        {
            "id": "U2500221",
            "name": "j565656",
            "quantity": 3,
            "price": 100,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365
        }
    ]
}

return_value = {"AWA234331237": {"lastStatusId": "76",
                                 "lastStatusName": "Тестовый статус",
                                 "lastStatusDate": "2023-04-25 11:01:08",
                                 "storeDate": None,
                                 "deliveryDate": "2023-05-10"}
                }
status_1 = {"AWA234331237": {"lastStatusId": "76",
                             "lastStatusName": "Доступен к получению в Пункте выдачи",
                             "lastStatusDate": "2023-04-25 11:01:08",
                             "storeDate": None,
                             "deliveryDate": "2023-05-10"}
            }
status_2 = {"AWA234331237": {"lastStatusId": "76",
                             "lastStatusName": "Успешно Выдан",
                             "lastStatusDate": "2023-04-25 11:01:08",
                             "storeDate": None,
                             "deliveryDate": "2023-05-10"}
            }


# class CreateOrderAPITest(TestCase):
#     """
#     Тестируем API создания заказа
#     """
#
#     def setUp(self):
#         self.data = test_data
#         self.invalid_data = invalid_data
#         self.url = "http://127.0.0.1:5000/api/create-order/"
#
#     def test_create_order_API_status_code(self):
#         r = requests.post(self.url, json=test_data)
#         self.assertEqual(201, r.status_code)
#
#     def test_create_order_API_status_code_with_invalid_data(self):
#         r = requests.post(self.url, json=test_data)
#         self.assertEqual(400, r.status_code)


class CreateOrderTest(TestCase):
    """
    Модульные тесты
    """
    maxDiff = None
    def setUp(self):
        self.items = [OrderedDict(
            [('product_id', 'U2500220'), ('name', 'jjjjj'), ('quantity', 5), ('price', 1000.0), ('height', 365),
             ('width', 256), ('depth', 235), ('weight', 2304)]),
            OrderedDict([('product_id', 'U2500221'), ('name', 'j565656'), ('quantity', 3), ('price', 100.0),
                         ('height', 365), ('width', 256), ('depth', 235), ('weight', 2304)])]

        self.boxes = [{'box': 1, 'items': [{'id': 'U2500220', 'name': 'jjjjj', 'qty': 5},
                                           {'id': 'U2500221', 'name': 'j565656', 'qty': 1}], 'cost': 1198.0,
                       'weight': 13824.0},
                      {'box': 2, 'items': [{'id': 'U2500221', 'name': 'j565656', 'qty': 2}], 'cost': 694.0,
                       'weight': 4608.0}]

        self.items = [
            {
                "product_id": "U2500220",
                "name": "jjjjj",
                "quantity": 5,
                "price": 1000,
                "weight": 2304,
                "depth": 235,
                "width": 256,
                "height": 365
            },
            {
                "product_id": "U2500221",
                "name": "j565656",
                "quantity": 3,
                "price": 100,
                "weight": 2304,
                "depth": 235,
                "width": 256,
                "height": 365
            }
        ]

    def test_replace_product_id_to_id(self):
        o = OrdersServices._replace_product_id_to_id(self.items)
        exist = [{'name': 'jjjjj', 'quantity': 5, 'price': 1000.0, 'height': 365, 'width': 256,
                  'depth': 235, 'weight': 2304, 'id': 'U2500220'},
                 {'name': 'j565656', 'quantity': 3, 'price': 100.0, 'height': 365, 'width': 256,
                  'depth': 235, 'weight': 2304, 'id': 'U2500221'}]

        self.assertEqual(exist, o)

    def test_count_declared_cost(self):
        o = OrdersServices._count_declared_cost(self.items)
        self.assertEqual(5300, o)

    def test_create_shipments(self):
        o = OrdersServices._create_shipments(self.boxes)
        exist = {"weight": 13824.0, "weight2": 4608.0}
        self.assertEqual(exist, o)

    def test_count_bin_and_costs_shipment(self):
        o = OrdersServices._count_bin_and_costs_shipment(products=self.items,
                                                         issue_point="5697",
                                                         pick_point="74070")
        exist = {'ISSUE_POINT': 5697, 'PICK_POINT': 74070,
                 'PICK_POINT_ADDRESS': '454010, Челябинск г, Дзержинского ул, д.92',
                 'total_cost': 1892.0, 'total_weight': 18432.0,
                 'boxes': [{'box': 1, 'items': [{'id': 'U2500220', 'name': 'jjjjj', 'qty': 5},
                                                {'id': 'U2500221', 'name': 'j565656', 'qty': 1}],
                            'cost': 1198.0, 'weight': 13824.0}, {'box': 2, 'items':
                     [{'id': 'U2500221', 'name': 'j565656', 'qty': 2}], 'cost': 694.0, 'weight': 4608.0}]}

        self.assertEqual(exist, o)

# def mocked_requests_get(*args, **kwargs):
#     """
#     Функция имитирует ответ API
#     """
#
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code
#
#         def json(self):
#             return self.json_data
#
#     return MockResponse(*args, **kwargs)
#
#
# class CheckStatusTest(TestCase):
#     def setUp(self) -> None:
#         self.product = Products.objects.create(
#             product_id=random.randrange(1000000000),
#             name="Носки 12345",
#             quantity="10",
#             price="10000"
#         )
#         self.order = Orders.objects.create(
#             order_id=f"Тестовый заказ {random.randrange(1000000000)}",
#             destination_point="12345",
#             departure_point="010",
#             fio="Тест Тестович тестов",
#             phone="79998887766",
#             email="test@test.test",
#             track_number="AWA234331237"
#
#         )
#         self.order.products.add(self.product)
#
#     @mock.patch('orders.boxberryAPI.BoxberryAPI.get_last_statuses',
#                 return_value=mocked_requests_get(return_value, 200))
#     def test_check_status_delivery_order(self, fake_response):
#         """
#         Тестируем, что новый статус заказа сохраняется в таблице бд
#         """
#         o = OrdersServices()
#         response = o.check_status_delivery_order()
#         exist = Orders.objects.get(track_number="AWA234331237")
#         self.assertEqual("Тестовый статус", exist.status)
#
#     @mock.patch('orders.boxberryAPI.BoxberryAPI.get_last_statuses',
#                 return_value=mocked_requests_get(status_1, 200))
#     def test_check_status_delivery_order_arrived(self, fake_response):
#         """
#         Тестируем, что если статус сменился на "Поступило в пункт выдачи",
#         будет отправлено уведомление
#         'Заказ № Тестовый заказ 195764352 готов к выдаче. Телефон: 88001005441. МК Электро'
#         """
#         o = OrdersServices()
#         o.check_status_delivery_order()
#
#     @mock.patch('orders.boxberryAPI.BoxberryAPI.get_last_statuses',
#                 return_value=mocked_requests_get(status_2, 200))
#     def test_check_status_delivery_order_issued(self, fake_response):
#         """
#         Тестируем, что если статус сменился на "Выдано",
#         будет отправлено уведомление
#         'Спасибо за покупку! Будем рады Вашему отзыву: https://mkelektro.ru/rev'
#         """
#         o = OrdersServices()
#         o.check_status_delivery_order()
