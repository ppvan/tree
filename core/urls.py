from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    CategoryProductView,
    DeleteProductView,
    DetailProductView,
    ListProductView,
    UpdateProductView,
    add_to_cart,
    cart_list,
    delete_cart_item,
    update_cart_item
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
    path("product/list/", ListProductView.as_view(), name="list_product"),
    path("product/<int:pk>/", DetailProductView.as_view(), name="detail_product"),
    path("product/<int:pk>/delete", DeleteProductView.as_view(), name="delete_product"),
    path("product/<int:pk>/update", UpdateProductView.as_view(), name="update_product"),
    path("product/category/", CategoryProductView.as_view(), name="category_product"),
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_list, name="cart"),
    path("delete-from-cart/", delete_cart_item, name="delete_from_cart"),
    path("update-from-cart/", update_cart_item, name="update_from_cart"),


    

]
