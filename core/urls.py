from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    AddToCartView,
    CartListView,
    DeleteProductView,
    DetailProductView,
    ListProductView,
    UpdateProductView,
    HomePageView,
    ProductByCategoryView,
    CategoryUpdateView,
    CategoryListView,
    CategoryCreateView,
    CategoryDeleteView,
)

app_name = "core"
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # Category
    path("category/list/", CategoryListView.as_view(), name="category_list"),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path("category/add/", CategoryCreateView.as_view(), name="category_add"),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path(
        "category/<slug:slug>/",
        ProductByCategoryView.as_view(),
        name="product_by_category",
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
    # Add to cart
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/list/", CartListView.as_view(), name="cart_list"),
]
