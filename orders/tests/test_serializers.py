import os
from _decimal import Decimal
from collections import OrderedDict

from django.test import SimpleTestCase, TestCase
# from unittest import TestCase
import random
import django
from rest_framework.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from orders.serializers import OrderProductsSerializer, OrdersSerializer


class OrderProductsTest(SimpleTestCase):

    def setUp(self) -> None:
        self.correct_data = {
            "id": 1010,
            "name": "Носки 12345",
            "quantity": 10,
            "price": 10000
        }
        self.data_with_invalid_field = {
            "id": 1010,
            1: 1991,
            "name": "Носки 12345",
            "quantity": 10,
            "price": 10000,
            "point": "Chl"
        }
        self.invalid_data = {
            "id": 1010,
            "name": "Носки 12345",
        }

    def test_order_product_serializer_witn_correct_data(self):
        o = OrderProductsSerializer(data=self.correct_data)
        o.is_valid(raise_exception=True)
        exist = OrderedDict(
            [('product_id', '1010'), ('name', 'Носки 12345'), ('quantity', 10), ('price', Decimal('10000.00'))])
        self.assertEqual(exist, o.validated_data)

    def test_order_product_serializer_with_invalid_field(self):
        o = OrderProductsSerializer(data=self.data_with_invalid_field)
        o.is_valid(raise_exception=True)
        exist = OrderedDict(
            [('product_id', '1010'), ('name', 'Носки 12345'), ('quantity', 10), ('price', Decimal('10000.00'))])
        self.assertEqual(exist, o.validated_data)

    def test_order_product_serializer_with_invalid_data(self):
        with self.assertRaises(ValidationError) as cm:
            o = OrderProductsSerializer(data=self.invalid_data)
            o.is_valid(raise_exception=True)

        self.assertEqual(ValidationError, cm.expected)


class OrdersSerializerTest(TestCase):

    def setUp(self):
        self.test_data = {'order_id': 'Тестовый заказ 46564', 'price': 2000.0, 'vid': '1',
                          'shop_name': '99451', 'shop_name1': '010', 'customer_fio': 'Иванов Иван Иванович',
                          'customer_phone': '+79001122322', 'customer_email': 'test@test.test',
                          'items': [
                              {'id': '252112-dget', 'name': 'Куртка детская', 'price': '1750', 'quantity': '1'},
                              {'id': '252113-dget', 'name': 'Носки', 'price': '1800', 'quantity': '2'}],
                          'weights_weight': '400', 'issue': '1'}

        self.invalid_field = {'order_id': 'Тестовый заказ 46564', 9999: 99999, 'price': 2000.0, 'vid': '1',
                              'shop_name': '99451', 'shop_name1': '010', 'customer_fio': 'Иванов Иван Иванович',
                              'customer_phone': '+79001122322', 'customer_email': 'test@test.test',
                              'items': [
                                  {'id': '252112-dget', 'name': 'Куртка детская', 'price': '1750', 'quantity': '1'},
                                  {'id': '252113-dget', 'name': 'Носки', 'price': '1800', 'quantity': '2'}],
                              'weights_weight': '400', 'issue': '1', 'ivvalid': 1}

        self.invalid_data = {'price': 2000.0, 'vid': '1',
                             'shop_name': '99451', 'shop_name1': '010', 'customer_fio': 'Иванов Иван Иванович',
                             'customer_phone': '+79001122322', 'customer_email': 'test@test.test',
                             'items': [
                                 {'id': '252112-dget', 'name': 'Куртка детская', 'price': '1750', 'quantity': '1'},
                                 {'id': '252113-dget', 'name': 'Носки', 'price': '1800', 'quantity': '2'}],
                             'weights_weight': '400', 'issue': '1'}

    def test_orders_serializer_with_correct_data(self):
        o = OrdersSerializer(data=self.test_data)
        o.is_valid(raise_exception=True)
        exist = OrderedDict([('order_id', 'Тестовый заказ 46564'),
                             ('price', Decimal('2000.00')),
                             ('vid', 1),
                             ('destination_point', '99451'),
                             ('departure_point', '010'),
                             ('fio', 'Иванов Иван Иванович'),
                             ('phone', '+79001122322'),
                             ('email', 'test@test.test'),
                             ('products',
                              [OrderedDict([('product_id', '252112-dget'),
                                            ('name', 'Куртка детская'),
                                            ('quantity', 1),
                                            ('price', Decimal('1750.00'))]),
                               OrderedDict([('product_id', '252113-dget'),
                                            ('name', 'Носки'),
                                            ('quantity', 2),
                                            ('price', Decimal('1800.00'))])])
                             ])

        self.assertEqual(exist, o.validated_data)

    def test_orders_serializer_with_invalid_field(self):
        o = OrdersSerializer(data=self.invalid_field)
        o.is_valid(raise_exception=True)
        exist = OrderedDict([('order_id', 'Тестовый заказ 46564'),
                             ('price', Decimal('2000.00')),
                             ('vid', 1),
                             ('destination_point', '99451'),
                             ('departure_point', '010'),
                             ('fio', 'Иванов Иван Иванович'),
                             ('phone', '+79001122322'),
                             ('email', 'test@test.test'),
                             ('products',
                              [OrderedDict([('product_id', '252112-dget'),
                                            ('name', 'Куртка детская'),
                                            ('quantity', 1),
                                            ('price', Decimal('1750.00'))]),
                               OrderedDict([('product_id', '252113-dget'),
                                            ('name', 'Носки'),
                                            ('quantity', 2),
                                            ('price', Decimal('1800.00'))])])
                             ])

        self.assertEqual(exist, o.validated_data)

    def test_orders_serializer_with_invalid_data(self):
        with self.assertRaises(ValidationError) as cm:
            o = OrdersSerializer(data=self.invalid_data)
            o.is_valid(raise_exception=True)

        self.assertEqual(ValidationError, cm.expected)
