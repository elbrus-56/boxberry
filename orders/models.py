from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models


class Orders(models.Model):
    type_of_delivery = [
        (1, 'ПВЗ'),
    ]

    order_id = models.CharField(primary_key=True, max_length=64)
    vid = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)],
                              choices=type_of_delivery, verbose_name="Тип доставки")
    destination_point = models.CharField(max_length=10)
    departure_point = models.CharField(max_length=10)
    customer_fio = models.CharField(max_length=255)
    customer_phone = models.CharField(validators=[MinLengthValidator(11)], max_length=12)
    customer_email = models.EmailField()
    track_number = models.CharField(max_length=64, blank=True)
    order_status = models.CharField(max_length=255, default="В обработке")
    items = models.ManyToManyField("Products", related_name="products_list", verbose_name="Список товаров")

    class Meta:
        db_table = "boxberry_orders"
        verbose_name = "Order Boxberry"
        verbose_name_plural = "Orders Boxberry"


class Products(models.Model):
    product_id = models.CharField(max_length=30)
    name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    height = models.IntegerField(validators=[MinValueValidator(0)])
    width = models.IntegerField(validators=[MinValueValidator(0)])
    depth = models.IntegerField(validators=[MinValueValidator(0)])
    weight = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = "boxberry_products"
        verbose_name = "Product Boxberry"
        verbose_name_plural = "Products Boxberry"
