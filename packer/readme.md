### Update 10.04.2023
- изменен формат входных данных (на уровне каждой позиции проставлен store - город с которого идет отгрузка
- введена предварительная группировка / разбивка заказов по городам, и последующее объединение


### Update 31.03.2023
- выделен отдельный app (packer)
- логика упаковки - в package.py
- 1 эндпойнт (packer/pack) ,  в который передается заданный json
- пример вызова packer/test.py


### Upgrades
- Функции разбивки на отправления вынесены в класс Package (package.py)
- Параметры габаритов и максимального веса по оператору доставки задаются в config.py (словарь передается в Packager при инициализации)
```
BOXBERRY_DELIVERY_CONFIG = {
    "max_width": 1850,
    "max_height": 1000,
    "max_depth": 800,
    "max_weight": 15000,
    "max_product_weight": 15000,
    "max_package_weight": 15000,
    "max_products": 3,
    "max_dimension_sum": 2500,
}
OZON_DELIVERY_CONFIG = {
    "max_width": 1790,
    "max_height": 790,
    "max_depth": 790,
    "max_weight": 25000,
    "max_product_weight": 0.8 * 25000,
    "max_package_weight": 0.9 * 25000,
    "max_products": 3,
    "max_dimension_sum": 0,
}


```
- Исходная точка отправления задается в DEFAULT_WAREHOUSE_ADDRESS в config.py
- В boxberry.py добавлена функция для расчета параметров отправления заказа целиком
    `def get_order_cost_and_delivery_time(self, order: Order):`

### Demo
`python3 test/test_packaging_boxberry.py`

- Демо берет доставленные заказы Ozon, достает из них город получателя (order['analytics_data']['city']), список продуктов. 
- По каждому продукту получает его вес и габариты
- Расчитывает необходимое количество коробок 
- Разбивает по коробкам
- Запускает по каждой коробке get_order_cost_and_delivery_time