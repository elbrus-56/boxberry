import json
from django.test import TestCase
from delivery.models import DeliveryData


test_subwords = [
    "a",
    "skdjfkjds",
    "б",
    "new york",
]
test_city_codes = [
    "68",
]
test_city_codes_wrong_data = [
    "023o432",
    "vnjf",
    "0234",
]

test_get_cost_and_date = [
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "010",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": 1,
        "start_date": "2022-08-08",
    }
]

test_get_cost_and_date_wrong_data = [
    # некорректный город отправления
    {
        "departure_city": "kjwere",
        "destination_city": "Москва",
        "address": "010",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": 1,
        "start_date": "2022-08-08",
    },
    # некорректный код ПВЗ
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "xyz",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": 1,
        "start_date": "2022-08-08",
    },
    # некорректные размеры
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "010",
        "height": -100,
        "width": 100,
        "depth": 100,
        "weight": 1,
        "start_date": "2022-08-08",
    },
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "010",
        "height": 100,
        "width": -100,
        "depth": 100,
        "weight": 1,
        "start_date": "2022-08-08",
    },
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "010",
        "height": 100,
        "width": 100,
        "depth": -100,
        "weight": 1,
        "start_date": "2022-08-08",
    },
    # некорректный вес
    {
        "departure_city": "Челябинск",
        "destination_city": "Москва",
        "address": "xyz",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": -1,
        "start_date": "2022-08-08",
    },
]


class DeliveryTest(TestCase):
    def test_getting_cities(self):
        for subword in test_subwords:
            result = self.client.get(f"/api/get-cities/{subword}/")
            self.assertEqual(result.status_code, 200)

    def test_getting_PPs(self):
        for city_code in test_city_codes:
            result = self.client.get(f"/api/get-PPs/{city_code}/")
            self.assertEqual(result.status_code, 200)

    def test_getting_PPs_wrong_data(self):
        for city_code in test_city_codes_wrong_data:
            result = self.client.get(f"/api/get-PPs/{city_code}/")
            self.assertEqual(result.status_code, 400)
            self.assertEqual(result.data, {"error": "Некорректный код"})

    def test_getting_cost_and_date(self):
        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date[0]),
            content_type="application/json",
        )
        self.assertEqual(result.status_code, 201)

    def test_getting_cost_and_date_wrong_data(self):
        # некорректный город отправления
        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[0]),
            content_type="application/json",
        )
        self.assertEqual(
            result.data,
            {"error": "Такого города нет в настройках или название невалидно"},
        )

        # некорректный код ПВЗ
        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[1]),
            content_type="application/json",
        )
        self.assertEqual(result.data, {"error": "Такого кода ПВЗ нет"})

        # некорректные размеры
        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[2]),
            content_type="application/json",
        )
        self.assertEqual(result.data["height"][0], "Высота не может быть отрицательной")

        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[3]),
            content_type="application/json",
        )
        self.assertEqual(result.data["width"][0], "Ширина не может быть отрицательной")

        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[4]),
            content_type="application/json",
        )
        self.assertEqual(result.data["depth"][0], "Глубина не может быть отрицательной")

        # некорректный вес
        result = self.client.post(
            "/api/create/",
            data=json.dumps(test_get_cost_and_date_wrong_data[5]),
            content_type="application/json",
        )
        self.assertEqual(result.data["weight"][0], "Вес не может быть отрицательным")
