import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm
from .models import Category, Order, OrderItem, Product
from .serializers import ModelSerializer


class PageTitleViewMixin:
    title = ""

    def get_title(self):
        """
        Return the class title attr by default.
        """
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        admin_group = user.groups.filter(name="Admins").exists()
        return user.is_superuser or admin_group


class AddProductView(
    AdminRequiredMixin,
    PageTitleViewMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Product
    form_class = ProductForm

    title = "Thêm sản phẩm"
    template_name = "core/product_add.html"
    success_url = reverse_lazy("core:list_products")
    success_message = "Sản phẩm %(name)s được thêm thành công"


class ListProductView(AdminRequiredMixin, ListView):
    model = Product
    template_name = "core/products_list.html"
    context_object_name = "products"


class DetailProductView(DetailView):
    model = Product
    template_name = "core/product_detail.html"


class UpdateProductView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "core/product_update.html"
    success_url = reverse_lazy("core:list_product")
    success_message = "Sản phẩm %(name)s đã được cập nhật thành công"


class DeleteProductView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = "core/product_delete.html"
    success_url = reverse_lazy("core:list_product")
    success_message = "Sản phẩm %(name)s đã được xóa thành công"


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request):
        payload = json.loads(request.body)

        product = get_object_or_404(Product, pk=payload["productId"])
        order, _created = Order.objects.get_or_create(
            user=request.user, state=Order.PENDING
        )
        order_item = self._update_item(order, product, payload["quantity"])

        serializer = ModelSerializer(order_item)
        return JsonResponse(serializer.to_dict(), status=200)

    def _update_item(self, order, product, quantity):
        order_item, _created = OrderItem.objects.get_or_create(
            order=order, product=product
        )
        order_item.quantity = quantity
        order_item.save()
        return order_item


def category_product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, "core/product_category.html", context)
