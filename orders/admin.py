from django.contrib import admin

from orders.models import Orders, Products


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
