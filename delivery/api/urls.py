from django.urls import path
from .views import *


app_name = "delivery"

urlpatterns = [
    path("get-cities/<str:subword>/", GetCityDataView.as_view(), name="get-cities"),
    path("get-PPs/<str:city_code>/", GetPPDataView.as_view(), name="get-PPs"),
    path("create/", CreateDDView.as_view(), name="create"),
    path("get-cities-geo/<str:city>", GetCitiesGeoView.as_view(), name="get-cities-geo"),
]
