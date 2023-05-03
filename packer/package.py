import requests
import json
from typing import List, Optional
import sys
import os
from loguru import logger
from email.message import EmailMessage
import smtplib
from py3dbp import Packer, Bin, Item
from dataclasses import dataclass, fields
from collections import defaultdict

parent = os.path.abspath(".")
sys.path.insert(1, parent)

logger.add("packer.log")


@dataclass
class PackageItem:
    id: str = ""
    code: str =''
    name: str = ""
    store: str =''
    width: int = 0
    height: int = 0
    depth: int = 0
    weight: int = 0
    qty: int = 0


@dataclass
class Posting:
    items: List[PackageItem]
    issue_point: str = ""
    pick_point: str = ""
    total_cost: int = 0
    total_weight: int = 0


@dataclass
class Order:
    packages: List[Posting]
    items: List[PackageItem]
    issue_point: str = ""
    pick_point: str = ""
    total_cost: int = 0
    total_weight: int = 0


@dataclass
class OperatorPackageLimit:
    max_width: int = 0
    max_height: int = 0
    max_depth: int = 0
    max_weight: int = 0
    max_product_weight: int = 0
    max_package_weight: int = 0
    max_products: int = 100
    max_dimension_sum: int = 0


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field


class PackageManager:
    def __init__(self, operator: dict):
        self.packer = Packer()
        self.result = True
        self.limits = dataclass_from_dict(OperatorPackageLimit, operator)

    def new_bin(self, bin_id: int = 0):
        """Creates new bin

        Args:
            bin_id (int, optional): bin id. Defaults to 0.

        Returns:
            Bin: new posting bin
        """
        return Bin(
            f"pack_{bin_id}",
            self.limits.max_width,
            self.limits.max_height,
            self.limits.max_depth,
            self.limits.max_weight,
        )

    def count_bins(self, items, max_bins: int = 100) -> int:
        """Calculate needed count bins for a given product list

        Args:
            products (list): list of products
            max_bins (int, optional): maximum bins allowed. Defaults to 100.

        Returns:
            int : count of bins needed
        """

        for box_no in range(max_bins):
            self.packer = Packer()
            for i in range(box_no):
                self.packer.add_bin(self.new_bin(box_no))
            for p in items:
                for q in range(p.qty):
                    self.packer.add_item(
                        Item(*[p.id, p.width, p.height, p.depth, p.weight])
                    )
            self.packer.pack(distribute_items=True)
            for b in self.packer.bins:
                if len(b.unfitted_items) == 0:
                    return box_no
        return max_bins

    def group_expanded_items(self, expanded_items):
        uniq = list({v['name']:v for v in expanded_items}.values())
        result = []
        for item in uniq:
            cnt = expanded_items.count(item)
            item['qty']=cnt
            result.append(item)
        return result

    def pack(self, order: Order, verbose=False):
        """Create list of packages for a given product list

        Args:
            products (list): product list from order
            verbose (bool, optional): output calculations to screen. Defaults to False.

        Returns:
            list of lists : [[offer_id_1, offer_id_2], [offer_id_2, offer_id_2]]
        """

        # products = [p["offer_id"], p["width"], p["height"], p["depth"], p["weight"]]

        # filter out heavy products to separate postings (4 goes for weight)
        if self.limits.max_dimension_sum != 0 and any(
            p.width + p.depth + p.height > self.limits.max_dimension_sum
            for p in order.items
        ):
            logger.error("At least one item is too big to fit in a maximum dimension")
            return []
        self.names = {o.id:o.name for o in order.items}
        self.codes = {o.id:o.code for o in order.items}
        if (
            len(order.items) > self.limits.max_products
            or sum([p.weight * p.qty for p in order.items])
            > self.limits.max_package_weight
        ):
            logger.error(
                "Overall number of products is too big for automatic processing. Do it manually"
            )
            postings = [
                [p.id]
                for p in order.items
                if p.weight >= self.limits.max_product_weight
            ]
            rest_products = [
                p for p in order.items if p.weight < self.limits.max_product_weight
            ]
        else:
            rest_products = order.items
            postings = []

        # calculate postings needed for the rest of products
        bins = self.count_bins(rest_products)

        # initialize packer
        self.packer = Packer()

        # add bins
        for bin_id in range(bins):
            self.packer.add_bin(self.new_bin(bin_id))

        # add products
        for p in rest_products:
            for q in range(p.qty):
                self.packer.add_item(Item(p.id, p.width, p.height, p.depth, p.weight))

        # distribute products among bins
        self.packer.pack(distribute_items=True, number_of_decimals=0)

        if verbose:
            print(f"Количество упаковок :{len(self.packer.bins)})")
            # если количество упаковок более 1шт то пока ручная обработка
            if len(self.packer.bins) > 1:
                self.result = False
            for i, b in enumerate(self.packer.bins):

                print(f"Упаковка {i}", b.string())

                print(f"Поместилось {len(b.items)} товаров")
                for item in b.items:
                    print(item.string())

                print(f"Не поместилось {len(b.unfitted_items)}:")
                for item in b.unfitted_items:
                    print("XXX", item.string())
        result = []
        box_id = 1
        for b in self.packer.bins:
            postings = []
            if len(b.items) > 0:
                postings = [
                    {
                        "id": item.name,
                        "code": self.codes[item.name],
                        "weight": item.weight,
                        "width": item.width,
                        "height": item.height,
                        "qty": 1,
                        "name": self.names[item.name],
                        "depth": item.depth,
                    }
                    for item in b.items
                ]

            result.append(
                {
                    "box": box_id,
                    "weight": b.get_total_weight(),
                    "width": b.width,
                    "height": b.height,
                    "depth": b.depth,
                    "items": self.group_expanded_items(postings),
                }
            )
            box_id += 1
        return result
