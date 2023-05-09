from django.urls import path

from .views import (
    DistrictView,
    GenerateAvatarView,
    ProductSearchView,
    ProvinceView,
    TransportFeeView,
    TransportServiceView,
    WardView,
)

app_name = "api"

urlpatterns = [
    path(
        "generate-avatar/<name>",
        GenerateAvatarView.as_view(),
        name="avatar_generate",
    ),
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("province/", ProvinceView.as_view(), name="province"),
    path("district/", DistrictView.as_view(), name="district"),
    path("ward/", WardView.as_view(), name="ward"),
    path(
        "transport-service/", TransportServiceView.as_view(), name="transport_service"
    ),
    path("transport-fee/", TransportFeeView.as_view(), name="transport_fee"),
]
