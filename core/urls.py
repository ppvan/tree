from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    DeleteProductView,
    DetailProductView,
    ListProductView,
    UpdateProductView,
)

app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("product/add/", AddProductView.as_view(), name="add_product"),
    path("product/list/", ListProductView.as_view(), name="list_product"),
    path("product/<int:pk>/", DetailProductView.as_view(), name="detail_product"),
    path("product/<int:pk>/delete", DeleteProductView.as_view(), name="delete_product"),
    path("product/<int:pk>/update", UpdateProductView.as_view(), name="update_product"),
]
