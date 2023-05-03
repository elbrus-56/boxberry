from uuid import UUID
from django.test import TestCase
from delivery.models import DeliveryData


class TestDeliveryDataModel(TestCase):
    def setUp(self):
        self.delivery_data1 = DeliveryData.objects.create(
            departure_city="Москва",
            destination_city="Санкт-Петербург",
            address="г. Москва, ул. Островитянова, д.34, к.2",
            height=100,  # высота отправления в мм
            width=100,
            depth=100,
            weight=10,  # вес в кг
            start_date="2022-09-02",
        )

    def test_delivery_data_can_be_created(self) -> None:
        delivery_data = self.delivery_data1
        self.assertEqual(str(delivery_data), 'Доставка из "Москва" в "Санкт-Петербург"')

    def test_delivery_data_uuid(self) -> None:
        delivery_data = self.delivery_data1
        self.assertEqual(type(delivery_data.id), UUID)

    def test_other_fields(self) -> None:
        delivery_data = self.delivery_data1
        self.assertEqual(delivery_data.height, 100)
        self.assertEqual(delivery_data.width, 100)
        self.assertEqual(delivery_data.depth, 100)
        self.assertEqual(delivery_data.weight, 10)
        self.assertEqual(delivery_data.start_date, "2022-09-02")

    def test_size_conversion(self) -> None:
        dd = self.delivery_data1
        height_cm, width_cm, depth_cm = dd.mm_to_cm_conversion(
            dd.height, dd.width, dd.depth
        )
        self.assertEqual(height_cm, 10.0)
        self.assertEqual(width_cm, 10.0)
        self.assertEqual(depth_cm, 10.0)

    def test_weight_conversion(self) -> None:
        dd = self.delivery_data1
        weight_gr = dd.kg_to_gr_conversion(dd.weight)
        self.assertEqual(weight_gr, 10000)
