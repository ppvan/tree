from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AddToCartForm, ProductForm
from .models import Category, Order, OrderItem, Product


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
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            product = get_object_or_404(Product, pk=product_id)
            order, _created = Order.objects.get_or_create(
                user=request.user, state=Order.PENDING
            )
            self._update_item(order, product, form.cleaned_data["quantity"])
            return redirect("core:cart_list")
        else:
            return HttpResponse("Fobidden", status=403)

    def _update_item(self, order, product, quantity):
        order_item, _created = OrderItem.objects.get_or_create(
            order=order, product=product
        )
        order_item.quantity = quantity
        order_item.save()
        return order_item


class CartListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "core/cart_list.html"
    context_object_name = "order_items"

    def get_queryset(self):
        order, _created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )
        return OrderItem.objects.filter(order=order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )[0]
        return context


def category_product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, "core/product_category.html", context)
