from django.conf import settings
from config.config import DEPARTURE_POINT_CODES
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser
from delivery.boxberry import Boxberry
from delivery.models import DeliveryData as DD
from delivery.models import PickPoint
from .serializers import CreateDDSerializer, DDSerializer


class GetCityDataView(APIView):
    """
    Эндпоинт для получения данных
    (имя, код) о городах по слову.
    """

    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, FormParser)

    def get(self, request: Request, subword: str) -> Response:
        boxberry = Boxberry(settings.BOXBERRY_TOKEN)
        list_of_cities = boxberry.get_list_of_cities_by_subword(subword)
        return Response(data=list_of_cities, status=status.HTTP_200_OK)

class GetCitiesGeoView(APIView):
    """
    Эндпоинт для получения данных
    (имя, код) о городах по слову.
    """

    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, FormParser)

    def get(self, request: Request, city: str) -> Response:
        try:
            pp = PickPoint.objects.filter(short_name=geo).first()
        except PickPoint.DoesNotExist:
               return Response({'Error':'City does not exist in database'}, status=404)
        else:
               return Response({'center_geo':pp.center_geo}, status=status.HTTP_200_OK)



class GetPPDataView(APIView):
    """
    Эндпоинт для получения данных о
    ПВЗ (PP), которые имеются в городе
    с указанным кодом
    """

    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, FormParser)

    def get(self, request: Request, city_code: str) -> Response:
        boxberry = Boxberry(settings.BOXBERRY_TOKEN)
        list_of_PP = boxberry.get_list_of_PP_by_city_code(city_code)
        if not list_of_PP:
            return Response(
                {"error": "Некорректный код"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=list_of_PP, status=status.HTTP_200_OK)


class CreateDDView(CreateAPIView):
    """
    Эндпоинт для получения данных о доставке
    с последующей записью в базу данных.
    """

    serializer_class = CreateDDSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, FormParser)

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        city_name = request.data["departure_city"]
        start_code = DEPARTURE_POINT_CODES.get(city_name.lower(), "")
        if start_code == "":
            msg = "Такого города нет в настройках" " или название невалидно"
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        # перевод единиц в формат, нужный для API Boxberry
        validated_data = serializer.validated_data

        height_cm, width_cm, depth_cm = DD.mm_to_cm_conversion(
            validated_data["height"], validated_data["width"], validated_data["depth"]
        )
        weight_gr = DD.kg_to_gr_conversion(validated_data["weight"])
        address = validated_data["address"]

        boxberry = Boxberry(settings.BOXBERRY_TOKEN)
        cost_and_delivery_time = boxberry.get_cost_and_delivery_time(
            weight=weight_gr,
            height=height_cm,
            depth=depth_cm,
            width=width_cm,
            start_code=start_code,
            end_code=address,
        )
        if list(cost_and_delivery_time.values()) == [0, 0, 0, 0]:
            return Response(
                {"error": "Такого кода ПВЗ нет"}, status=status.HTTP_400_BAD_REQUEST
            )

        delivery_data = serializer.save()
        delivery_data.cost_of_delivery = cost_and_delivery_time["price"]
        delivery_days = cost_and_delivery_time["delivery_period"]
        delivery_data.end_date = delivery_data.add_multiple_days(delivery_days)
        delivery_data.save()
        serializer = DDSerializer(delivery_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
