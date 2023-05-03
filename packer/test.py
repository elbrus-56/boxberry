import json
import requests

BASE_URL = "http://127.0.0.1:5000"
js = {
    # "ISSUE_POINT": 74070,
    "PICK_POINT": 96051,
    "order": [
        {
            "id": "U2500220",
            "code": "U250022022",
            "name": "jjjjj",
            "store": "ЧЛБ",
            "qty": 25,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365,
        },
        {
            "id": "U2500221",
            "code": "U2210022021",
            "name": "j565656",
            "store": "ЕКБ-2",
            "qty": 32,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365,
        },
        {
            "id": "U2500220",
            "code": "U250022023",
            "name": "jjjjj",
            "store": "ЕКБ-3",
            "qty": 15,
            "weight": 2304,
            "depth": 235,
            "width": 256,
            "height": 365,
        },
    ],
}
r = requests.post(
    BASE_URL + "/packer/pack", json=js, headers={"Accept-Type": "application/json"}
)
print(r.text)
print(json.dumps(r.json(), indent=4, ensure_ascii=False, default=str))
