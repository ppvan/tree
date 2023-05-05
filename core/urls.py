from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    AddToCartView,
    CartListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    CheckoutView,
    DeleteProductView,
    DetailProductView,
    HomePageView,
    ProductByCategoryView,
    ProductListView,
    UpdateProductView,
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
    path("product/add/", AddProductView.as_view(), name="product_add"),
    path("product/list/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", DetailProductView.as_view(), name="product_detail"),
    path("product/<int:pk>/delete", DeleteProductView.as_view(), name="product_delete"),
    path("product/<int:pk>/update", UpdateProductView.as_view(), name="product_update"),
    # Add to cart
    path("cart/add/", AddToCartView.as_view(), name="cart_add"),
    path("cart/list/", CartListView.as_view(), name="cart_list"),
    # Checkout
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
