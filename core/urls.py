from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    AddToCartView,
    DeleteProductView,
    DetailProductView,
    ListProductView,
    UpdateProductView,
    category_product,
)

app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "category/list/",
        TemplateView.as_view(template_name="admin/list_category.html"),
        name="list_catagory",
    ),
    path(
        "post/list/",
        TemplateView.as_view(template_name="admin/list_post.html"),
        name="list_post",
    ),
    path("product/add/", AddProductView.as_view(), name="add_product"),
    path("product/list/", ListProductView.as_view(), name="list_products"),
    path("product/<int:pk>/", DetailProductView.as_view(), name="detail_product"),
    path("product/<int:pk>/delete", DeleteProductView.as_view(), name="delete_product"),
    path("product/<int:pk>/update", UpdateProductView.as_view(), name="update_product"),
    path("product/category", category_product, name="category_product"),
    # Add to cart
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
]
