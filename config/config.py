DEPARTURE_POINT_CODES = {
    "челябинск": "74070",
    "екатеринбург": "96051",
}
# Credentials
DEFAULT_WAREHOUSE_ADDRESS = "Челябинск"
BOXBERRY_API_KEY = "9388294190e51ba4966c6bf3b0695b66"
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
