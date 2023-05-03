import json
import sys
import os

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from boxberry import Boxberry
from package import PackageManager, PackageItem, Order
from config import (
    DEFAULT_WAREHOUSE_ADDRESS,
    BOXBERRY_DELIVERY_CONFIG,
    BOXBERRY_API_KEY,
)


def test_boxberry_packaging():
    bb = Boxberry(BOXBERRY_API_KEY)
    pm = PackageManager(operator=BOXBERRY_DELIVERY_CONFIG)

    with open("product_dimensions.json", "r") as inp:
        product_dimensions = json.loads(inp.read())
    with open("test_orders.json", "r") as inp:
        req = json.loads(inp.read())
    for o in req["result"]["postings"]:
        items = []
        for product in o["products"]:
            product_id = product["offer_id"]
            item = PackageItem(
                product_id=product_id,
                width=product_dimensions[product_id]["width"],
                height=product_dimensions[product_id]["height"],
                depth=product_dimensions[product_id]["depth"],
                weight=product_dimensions[product_id]["weight"],
            )
            items.append(item)

        dest = o["analytics_data"]["city"]
        if not dest:
            dest = o["analytics_data"]["region"]

        order = Order(
            items=items, source=DEFAULT_WAREHOUSE_ADDRESS, destination=dest, packages=[]
        )

        postings = pm.pack(order)

        if len(postings) == 0:
            continue

        order.packages = [a["products"] for a in postings]

        src_cty = bb.get_list_of_cities_by_subword(DEFAULT_WAREHOUSE_ADDRESS)
        src_code = src_cty[0]["Code"]

        dest_cty = bb.get_list_of_cities_by_subword(dest)
        if len(dest_cty) == 0:
            continue
        else:
            dest_code = dest_cty[0]["Code"]
        order.source = src_code
        order.destination = dest_code
        res = bb.get_order_cost_and_delivery_time(order)
        print("Заказ:", order)
        print("-" * 30)
        print("Отправления:", postings)
        print("-" * 30)

        print("Стоимость доставки", res)
        print()
        print("=" * 30)


test_boxberry_packaging()
