import json
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser
from delivery.boxberry import Boxberry
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .serializers import OrderSerializer, PackageSerializer
from .package import PackageManager, PackageItem, Order
from config.config import (
    BOXBERRY_DELIVERY_CONFIG,
    BOXBERRY_API_KEY,
)
from delivery.models import PickPoint

def get_ip_code(short_city_name:str)->int:
    if '-' in short_city_name:
       short_city_name = short_city_name.split('-')[0]
    ip = PickPoint.objects.filter(short_name=short_city_name).first()
    if ip:
       return ip.pick_point
    else:
       return False


class PackOrderView(APIView):
    """
    Эндпоинт для разбиения заказа на отправления, и расчета стоимости

    """

    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)


    @swagger_auto_schema(request_body=OrderSerializer, responses={200:PackageSerializer})
    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        boxberry = Boxberry(BOXBERRY_API_KEY)
        pm = PackageManager(operator=BOXBERRY_DELIVERY_CONFIG)

        #ISSUE_POINT = request.data["ISSUE_POINT"]
        PICK_POINT = request.data["PICK_POINT"]
        request_order = request.data["order"]
        stores = list(set([o['store'] for o in request_order]))
        order_items = [PackageItem(**o) for o in request_order]
        order_packages=[]
        total_cost = 0
        total_weight = 0
        for store in stores:
            store_order_items =  [PackageItem(**o) for o in request_order if o['store']==store]
            issue_point = get_ip_code(store)

            if not issue_point:
               raise Exception(f'Issue point for {store} not found')
               continue
            order = Order(
                items=store_order_items,
                issue_point=issue_point, # ????
                pick_point=PICK_POINT,
                packages=[],
            )

            postings = pm.pack(order, verbose=True)

            if len(postings) == 0:
                return Response({"Error": "Order is empty"})
            else:
                order.packages = [
                    {
                        "box": a["box"],
                        "items": a["items"],
                        "weight": a["weight"],
                        "height": a["height"],
                        "width": a["width"],
                        "depth": a["depth"],
                    }
                    for a in postings
                ]
                res = boxberry.get_order_cost_and_delivery_time(order)
                order.packages = {'city':store, "boxes":[
                    {
                        "box": a["box"],
                        "items": a["items"],
                        "cost": res["costs"][i]["price"],
                        "weight": a["weight"],
                    }
                    for i, a in enumerate(postings)
                ]}

                total_cost += res["total_cost"]
                total_weight += res["total_weight"]
               
                order_packages.append(order.packages)
        order_data = {
                #"ISSUE_POINT": ISSUE_POINT,
                "PICK_POINT": PICK_POINT,
                "PICK_POINT_ADDRESS": boxberry.get_pvz_address(PICK_POINT),
                "total_cost": total_cost,
                "total_weight": total_weight,
                "logistics": order_packages,
            }
        print(json.dumps(order_data, indent=4, ensure_ascii=False, default=str  ))
        serializer = PackageSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
