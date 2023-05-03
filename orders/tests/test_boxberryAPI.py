import os
from unittest import mock

from django.test import SimpleTestCase
# from unittest import TestCase
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from orders.boxberryAPI import BoxberryAPI

test_data = {
    "order_id": f"Тестовый заказ {random.randrange(10000, 100000)}",
    "price": 2000.00,  # Объявленная стоимость отправления. По умолчанию значение будет 5 руб.
    "vid": "1",  # Вид доставки 1,2,3
    "shop": {  # Блок с информацией о пункте приема и пункте выдачи отправления
        "name": "99451",  # Код пункта выдачи
        "name1": "010"  # Код пункта поступления
    },
    "customer": {  # Блок с информацией о получателе отправления
        "fio": "Иванов Иван Иванович",
        "phone": "+79001122322",
        "email": "test@test.test"
    },
    "items": [{  # Блок с информацией по товарным позициям, включённым в заказ.
        "id": "252112-dget",  # Необязательное поле
        "name": "Куртка детская",
        "price": "1750",
        "quantity": "1",
    },
        {  # Блок с информацией по товарным позициям, включённым в заказ.
            "id": "252113-dget",  # Необязательное поле
            "name": "Носки",
            "price": "1800",
            "quantity": "2",
        }
    ],
    "weights": {  # Блок с информацией о тарных местах
        "weight": "400",
    },
    "issue": "1"  # Вид выдачи заказа, возможные значения: 0,1,2
}
test_data_2 = {
    "order_id": f"Тестовый заказ {random.randrange(10000, 100000)}",
    "price": 2000.00,  # Объявленная стоимость отправления. По умолчанию значение будет 5 руб.
    "vid": "1",  # Вид доставки 1,2,3
    "shop": {  # Блок с информацией о пункте приема и пункте выдачи отправления
        "name": "99451",  # Код пункта выдачи
        "name1": "010"  # Код пункта поступления
    },
    "customer": {  # Блок с информацией о получателе отправления
        "fio": "Иванов Иван Иванович",
        "phone": "+79001122322",
        "email": "test@test.test"
    },
    "items": [{  # Блок с информацией по товарным позициям, включённым в заказ.
        "id": "252112-dget",  # Необязательное поле
        "name": "Куртка детская",
        "price": "1750",
        "quantity": "1",
    },
        {  # Блок с информацией по товарным позициям, включённым в заказ.
            "id": "252113-dget",  # Необязательное поле
            "name": "Носки",
            "price": "1800",
            "quantity": "2",
        }
    ],
    "weights": {  # Блок с информацией о тарных местах
        "weight": "400",
    },
    "issue": "1"  # Вид выдачи заказа, возможные значения: 0,1,2
}
invalid_data = {
    "order_id": f"Тестовый заказ {random.randrange(10000, 100000)}",
    "vid": "1",  # Вид доставки 1,2,3
    "shop": {  # Блок с информацией о пункте приема и пункте выдачи отправления
        "name": "99451",  # Код пункта выдачи
        "name1": "010"  # Код пункта поступления
    },
    "customer": {  # Блок с информацией о получателе отправления
        "fio": "Иванов Иван Иванович",
        "phone": "+79001122322",
        "email": "test@test.test"
    },
    "items": [{  # Блок с информацией по товарным позициям, включённым в заказ.
        "id": "252112-dget",  # Необязательное поле
        "name": "Куртка детская",
        "price": "1750",
        "quantity": "1",
    },
        {  # Блок с информацией по товарным позициям, включённым в заказ.
            "id": "252113-dget",  # Необязательное поле
            "name": "Носки",
            "price": "1800",
            "quantity": "2",
        }
    ],
    "weights": {  # Блок с информацией о тарных местах
        "weight": "",  # Для теста с неправильными данными установлено пустое значение
    },
    "issue": "1"  # Вид выдачи заказа, возможные значения: 0,1,2
}


class BoxberryAPITest(SimpleTestCase):

    def setUp(self):
        self.correct_data = test_data_2
        self.invalid_data = invalid_data

        self.track_number_correct = "AWA234331237"
        self.track_number_invalid = ""

        self.ParselCreate_correct = {
            "method": "ParselCreate",
            "sdata": test_data
        }

        self.ParselCreate_invalid = {
            "method": "ParselCreate",
            "sdata": invalid_data
        }

        self.LastStatuses_correct = {
            "method": "GetLastStatusData",
            "trackNumbers": ["AWA234331237"]
        }

        self.LastStatuses_invalid = {
            "method": "GetLastStatusData",
            "trackNumbers": [""]
        }

    def test_post_api_with_parsel_create_correct(self):
        """
        При вызове функция создаст реальное отправление
        в личном кабинете Boxberry.
        """
        o = BoxberryAPI()
        response = o.post_api(self.ParselCreate_correct)
        exist = {'label': response.json()["label"],
                 'track': response.json()["track"]
                 }
        self.assertEqual(exist, response.json())

    def test_post_api_with_parsel_create_invalid(self):
        o = BoxberryAPI()
        response = o.post_api(self.ParselCreate_invalid)
        self.assertEqual(None, response)

    def test_post_api_with_last_status_correct(self):
        o = BoxberryAPI()
        response = o.post_api(self.LastStatuses_correct)
        print("test_post_api_with_list_status_correct: ", response.json())

    def test_post_api_with_last_status_invalid(self):
        o = BoxberryAPI()
        response = o.post_api(self.LastStatuses_invalid)
        self.assertEqual(None, response)

    def test_send_request_to_create_order_correct(self):
        """
            При вызове функция создаст реальное отправление
            в личном кабинете Boxberry.
        """
        o = BoxberryAPI()
        response = o.send_request_to_create_order(self.correct_data)
        exist = {'track': response.json()["track"],
                 'label': response.json()["label"]}

        self.assertEqual(exist, response.json())

    def test_send_request_to_create_order_invalid(self):
        o = BoxberryAPI()
        response = o.send_request_to_create_order(self.invalid_data)
        self.assertEqual(None, response)

    def test_get_list_statuses_correct(self):
        o = BoxberryAPI()
        response = o.get_last_statuses(self.track_number_correct)
        print("test_get_list_statuses_correct: ", response.json())

    def test_get_list_statuses_invalid(self):
        o = BoxberryAPI()
        response = o.get_last_statuses(self.track_number_invalid)
        self.assertEqual(None, response)
