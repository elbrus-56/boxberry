from django.db import models
from datetime import timedelta, date
from .mixins import UUIDModel, TimeStamp


class DeliveryData(UUIDModel, TimeStamp):
    departure_city = models.CharField(max_length=255, verbose_name="Город отправления")
    destination_city = models.CharField(max_length=255, verbose_name="Город назначения")
    address = models.CharField(max_length=512, verbose_name="ПВЗ или адрес для курьера")
    height = models.IntegerField(verbose_name="Высота коробки, мм")
    width = models.IntegerField(verbose_name="Ширина коробки, мм")
    depth = models.IntegerField(verbose_name="Глубина коробки, мм")
    weight = models.IntegerField(verbose_name="Вес поссылки в килограммах")
    start_date = models.DateField(verbose_name="Дата передачи в доставку")

    end_date = models.DateField(blank=True, null=True, verbose_name="Дата доставки")
    cost_of_delivery = models.IntegerField(
        blank=True, null=True, verbose_name="Стоимость доставки"
    )

    class Meta:
        verbose_name = "Данные доставки"
        verbose_name_plural = "Данные доставок"

    def __str__(self) -> str:
        return f'Доставка из "{self.departure_city}" в "{self.destination_city}"'

    @staticmethod
    def mm_to_cm_conversion(height, width, depth) -> tuple:
        return (height / 10, width / 10, depth / 10)

    @staticmethod
    def kg_to_gr_conversion(weight) -> int:
        return weight * 1000

    def add_multiple_days(self, days: int) -> str:
        end_date = self.start_date + timedelta(days=days)
        return str(end_date)

class PickPoint(models.Model):
    id = models.CharField(verbose_name="Код города в Боксберри", max_length=20)
    center_geo = models.CharField(max_length=64, verbose_name="Геометка центральной точки")
    pick_point = models.IntegerField(verbose_name="Код точки приема заказа", primary_key=True)
    short_name = models.CharField(max_length=4, verbose_name="Короткое название города")
    full_name =  models.CharField(max_length=64, verbose_name="Полное название города")

    class Meta:
        verbose_name = "Точка приема посылок"
        verbose_name_plural = "Точки приема посылок"

    def __str__(self) -> str:
        return f'{self.short_name}-{self.pick_point}'