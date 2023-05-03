from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from delivery.models import DeliveryData


class DDSerializer(ModelSerializer):
    """Serializer for get-views"""

    class Meta:
        model = DeliveryData  # DeliveryData = DD
        fields = "__all__"


class CreateDDSerializer(ModelSerializer):
    """Serializer for creation"""

    end_date = serializers.DateField(read_only=True)
    cost_of_delivery = serializers.IntegerField(read_only=True)

    weight = serializers.IntegerField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()
    depth = serializers.IntegerField()

    class Meta:
        model = DeliveryData
        fields = (
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
        )

    def validate_weight(self, value):
        weight = self.get_initial().get("weight")
        if weight == "":
            raise ValidationError("Это поле не должно быть пустым")
        if weight <= 0:
            raise ValidationError("Вес не может быть отрицательным")
        return value

    def validate_height(self, value):
        height = self.get_initial().get("height")
        if height == "":
            raise ValidationError("Это поле не должно быть пустым")
        if height <= 0:
            raise ValidationError("Высота не может быть отрицательной")
        return value

    def validate_width(self, value):
        width = self.get_initial().get("width")
        if width == "":
            raise ValidationError("Это поле не должно быть пустым")
        if width <= 0:
            raise ValidationError("Ширина не может быть отрицательной")
        return value

    def validate_depth(self, value):
        depth = self.get_initial().get("depth")
        if depth == "":
            raise ValidationError("Это поле не должно быть пустым")
        if depth <= 0:
            raise ValidationError("Глубина не может быть отрицательной")
        return value
