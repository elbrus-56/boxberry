from django.test import TestCase
from django.conf import settings
from delivery.boxberry import Boxberry


class TestDeliveryDataModel(TestCase):
    def setUp(self):
        self.boxberry = Boxberry(settings.BOXBERRY_TOKEN)

    def test_getting_multiple_cities(self) -> None:
        list_of_cities = self.boxberry.get_list_of_cities_by_subword("а")
        self.assertTrue(len(list_of_cities) <= 10)
        for city in list_of_cities:
            self.assertEquals(city["Name"][0].lower(), "а")
            self.assertListEqual(list(city.keys()), ["Name", "Code"])

    def test_getting_multiple_PP(self) -> None:
        list_of_PP = self.boxberry.get_list_of_PP_by_city_code("68")
        self.assertTrue(len(list_of_PP) <= 10)
        for PP in list_of_PP:
            self.assertListEqual(list(PP.keys()), ["Code", "Address", "Name"])

    def test_getting_cost_and_delivery_time(self) -> None:
        result = self.boxberry.get_cost_and_delivery_time(
            100, 20, 20, 20, "74070", "96051"
        )
