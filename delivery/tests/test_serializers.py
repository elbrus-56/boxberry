from django.test.testcases import TestCase
from delivery.models import DeliveryData
from delivery.api.serializers import DDSerializer


valid_data = [
    {
        "departure_city": "Москва",
        "destination_city": "Санкт-Петербург",
        "address": "г. Москва, ул. Островитянова, д.34, к.2",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": 1000,
        "start_date": "2022-01-01",
    },
]

invalid_data = [
    {
        "departure_city": "Москва",
        "destination_city": "Санкт-Петербург",
        "address": "г. Москва, ул. Островитянова, д.34, к.2",
        "height": 100,
        "width": 100,
        "depth": 100,
        "weight": 1000,
        "start_date": "2022-01-01",
    }
]


class TestSerializers(TestCase):
    """
    Тестируем два сериализатора: один нужен для создания,
    другой - для получения данных из БД. В первой функции
    тестируем первый сериализатор с верными и неверными
    данными
    """

    def setUp(self):
        self.dd_serializer = DDSerializer(data=valid_data[0])

    def test_serializer(self) -> None:
        serializer = self.dd_serializer
        self.assertTrue(serializer.is_valid())

    def test_serializer_data(self) -> None:
        serializer = self.dd_serializer
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        self.assertCountEqual(
            data.keys(),
            [
                "created_at",
                "updated_at",
                "departure_city",
                "destination_city",
                "address",
                "height",
                "width",
                "depth",
                "weight",
                "start_date",
                "end_date",
                "cost_of_delivery",
            ],
        )
        self.assertEqual(data["departure_city"], "Москва")
        self.assertEqual(data["destination_city"], "Санкт-Петербург")
