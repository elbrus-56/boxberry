from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    code = serializers.CharField()
    store = serializers.CharField()
    qty = serializers.IntegerField()
    weight = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    depth = serializers.IntegerField()



class OrderSerializer(serializers.Serializer):
    #ISSUE_POINT = serializers.IntegerField()
    PICK_POINT = serializers.IntegerField()
    order = serializers.ListField(child=OrderItemSerializer())


class BoxItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    code = serializers.CharField()
    qty = serializers.IntegerField()


class CitySerializer(serializers.Serializer):
    city = serializers.CharField()
    boxes = serializers.ListField(child=BoxItemSerializer())


class BoxSerializer(serializers.Serializer):
    box = serializers.IntegerField()
    items = serializers.ListField(child=BoxItemSerializer())
    cost = serializers.FloatField()
    weight = serializers.FloatField()

class CitySerializer(serializers.Serializer):
    city = serializers.CharField()
    boxes = serializers.ListField(child=BoxSerializer())


class PackageSerializer(serializers.Serializer):
    #ISSUE_POINT = serializers.IntegerField()
    PICK_POINT = serializers.IntegerField()
    PICK_POINT_ADDRESS = serializers.CharField(required=False)
    total_cost = serializers.FloatField()
    total_weight = serializers.FloatField()
    logistics = serializers.ListField(child=CitySerializer())
