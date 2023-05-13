from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AddProductView,
    AddToCartView,
    AdminOrderListView,
    BugReportView,
    CartListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    CheckoutView,
    DeleteProductView,
    DetailProductView,
    HomePageView,
    OrderCancelView,
    OrderCompletedView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
    ProductByCategoryView,
    ProductListView,
    ProductUpdateView,
    UpdateCartView,
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
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    # Add to cart
    path("cart/add/", AddToCartView.as_view(), name="cart_add"),
    path("cart/update/", UpdateCartView.as_view(), name="cart_update"),
    path("cart/list/", CartListView.as_view(), name="cart_list"),
    # Order
    path("order/checkout/", CheckoutView.as_view(), name="checkout"),
    path("order/list/", OrderListView.as_view(), name="order_list"),
    path("order/admin-list/", AdminOrderListView.as_view(), name="admin_order_list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("order/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path(
        "order/<int:pk>/completed", OrderCompletedView.as_view(), name="order_completed"
    ),
    path("order/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("order/<int:pk>/cancel", OrderCancelView.as_view(), name="order_cancel"),
    path(
        "bug/report",
        BugReportView.as_view(),
        name="bug_report",
    ),
]
