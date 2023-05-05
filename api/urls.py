from django.urls import path

from .views import (
    DistrictView,
    ProductSearchView,
    ProvinceView,
    TransportFeeView,
    TransportServiceView,
    WardView,
)

app_name = "api"

urlpatterns = [
    path("search/", ProductSearchView.as_view(), name="product_seach"),
    path("province/", ProvinceView.as_view(), name="province"),
    path("district/", DistrictView.as_view(), name="district"),
    path("ward/", WardView.as_view(), name="ward"),
    path(
        "transport-service/", TransportServiceView.as_view(), name="transport_service"
    ),
    path("transport-fee/", TransportFeeView.as_view(), name="transport_fee"),
]
