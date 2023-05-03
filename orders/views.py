from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from orders.serializers import OrderSerializer
from orders.services.orders import OrdersServices


class CreateOrdersView(CreateAPIView):
    """
    Эндпоинт для создания нового заказа Boxberry
    """

    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        response = OrdersServices().create_order(validated_data)

        if response:
            new_order = serializer.save()
            new_order.track_number = response["track"]
            new_order.save()
            return Response({f"Отправление {new_order.track_number} успешно создано"},
                            status=status.HTTP_201_CREATED)

        return Response({'err': f"Произошла ошибка. Отправление для заказа {serializer.validated_data['order_id']}"
                                f" не было создано."}, status=status.HTTP_400_BAD_REQUEST)

