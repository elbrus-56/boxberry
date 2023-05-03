import os

from django.test import TestCase
# from unittest import TestCase
from unittest.mock import MagicMock
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from orders.models import Products, Orders


class OrdersTest(TestCase):

    def setUp(self):
        """
        Создаем записи в тестовой БД
        """

        self.statuses = [
            "В обработке",
            "Принято к доставке",
            "Передано на сортировку",
            "Отправлен на сортировочный терминал",
            "Отправлено в город назначения",
            "Передан на доставку до пункта выдачи",
            "Передано на курьерскую доставку",
            "Поступило в пункт выдачи",
            "Выдано",
            "Возвращено с курьерской доставки",
            "Готовится к возврату",
            "Отправлено в пункт приема",
            "Возвращено в пункт приема",
            "Возвращено в ИМ"
        ]
        for i in range(len(self.statuses)):
            self.product = Products.objects.create(
                product_id=random.randrange(1000000000),
                name="Носки 12345",
                quantity="10",
                price="10000"
            )
            self.order = Orders.objects.create(
                order_id=f"Тестовый заказ {random.randrange(1000000000)}",
                destination_point="12345",
                departure_point="010",
                fio="Тест Тестович тестов",
                phone="79998887766",
                email="test@test.test",
                track_number="AAP246015199",
                status=self.statuses[i],

            )
            self.order.products.add(self.product)

    def test_create_record_in_models(self):
        order = Orders.objects.all()
        self.assertEqual(14, len(order))
