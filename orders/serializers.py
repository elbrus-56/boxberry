from rest_framework import serializers
from orders.models import Orders, Products


class OrderProductsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="product_id")

    class Meta:
        model = Products
        fields = ["id", "name", "quantity", "price", "height", "width", "depth", "weight"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderProductsSerializer(many=True)

    class Meta:
        model = Orders
        fields = ["order_id", "destination_point", "departure_point", "customer_fio",
                  "customer_phone", "customer_email", "items"]

    def create(self, validated_data):
        products = validated_data.pop("items")
        order = Orders.objects.create(**validated_data)
        order.save()
        for product in products:
            prod = Products.objects.create(**product)
            prod.save()
            order.items.add(prod)
        return order
