import requests


class Boxberry:
    """
    Класс для взаимодействия с Boxberry API.Ссылка на документацию:
    https://help.boxberry.ru/pages/viewpage.action?pageId=762955
    """

    PREFIX = "https://api.boxberry.ru/json.php"
    COUNTRIES = {"Russia": "643"}

    def __init__(self, token: str, country: str = "Russia") -> None:
        self.token = token
        self.country = country

    def get_list_of_cities_by_subword(
        self, subword: str, number_of_cities: int = 10
    ) -> list:
        """
        Получение нескольких городов с ПВЗ,
        в названии которых имеется часть subword
        """
        result = []
        url = f"{self.PREFIX}?token={self.token}&method=ListCitiesFull&CountryCode=643"
        response = requests.get(url)
        list_of_cities = response.json()

        for city in list_of_cities:
            if city["Name"].lower().startswith(subword.lower()):
                shortened = {"Name": city["Name"], "Code": city["Code"]}
                result.append(shortened)
                if len(result) == number_of_cities:
                    break
        return result


    def get_list_of_PP_by_city_code(
        self, city_code: str, number_of_PP: int = 10
    ) -> list:
        """
        Получение нескольких (10 по умолчанию)
        ПВЗ для города с кодом town.
        """
        result = []
        url = f"{self.PREFIX}?token={self.token}&method=ListPoints&prepaid=1&CityCode={city_code}&CountryCode=643"
        response = requests.get(url)
        list_of_PP = response.json()

        if "err" in list_of_PP[0].keys():
            return

        for PP in list_of_PP:
            shortened = {
                "Code": PP["Code"],
                "Address": PP["Address"],
                "Name": PP["Name"],
                "Geo" : PP['GPS']
            }
            result.append(shortened)
            if len(result) == number_of_PP:
                break
        return result
    # https://api.boxberry.ru/json.php?token=d6f33e419c16131e5325cbd84d5d6000&method=PointsDescription&code=75059&photo=1
    def get_pvz_address(self, pvz_code:int):
        params = {"token":self.token,
                  "method":"PointsDescription",
                  "code":pvz_code}
        response = requests.get(self.PREFIX, params)
        if response.status_code == 200:
            return response.json().get('Address','Address unknown')
        return ''

    def get_cost_and_delivery_time(
        self,
        weight: int,
        height: int,
        width: int,
        depth: int,
        start_code: str,
        end_code: str,
    ) -> dict:

        """Расчет стоимости и времени доставки"""
        params = {
            "token": self.token,
            "method": "DeliveryCosts",
            "weight": weight,
            "width": width,
            "depth": depth,
            "height": height,
            "targetstart": start_code,
            "target": end_code,
        }

        response = requests.get(self.PREFIX, params)
        return response.json()

    def get_order_cost_and_delivery_time(self, order):
        costs = []
        for item in order.packages:
            cost = self.get_cost_and_delivery_time(
                item["weight"],
                item["height"],
                item["width"],
                item["depth"],
                order.issue_point,
                order.pick_point,
            )
            if 'err' not in cost.keys():
               costs.append(cost)
            else:
               costs.append({})

        total_cost = sum([a.get("price",0) for a in costs if a])
        total_weight = sum([item['weight'] for item in order.packages])
        return {"total_cost": total_cost, "total_weight": total_weight, "costs": costs}
