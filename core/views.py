import json
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models.query import QuerySet
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
    QueryDict,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from blog.models import Post

from .forms import (
    AddToCartForm,
    BugReportForm,
    CategoryForm,
    CheckoutForm,
    OrderFilterForm,
    OrderForm,
    ProductForm,
)
from .models import Address, Category, Order, OrderItem, Product


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
    success_url = reverse_lazy("core:product_list")
    success_message = "Sản phẩm %(name)s được thêm thành công"


class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = "core/products_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.order_by("-updated_at")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not context.get("is_paginated", False):
            return context

        paginator = context.get("paginator")
        num_pages = paginator.num_pages
        current_page = context.get("page_obj")
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({"pages": pages})
        return context


class DetailProductView(DetailView):
    model = Product
    template_name = "core/product_detail.html"

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if product.is_deleted:
            raise Http404("Sản phẩm không tồn tại")

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.order_by("label")[:8]
        return context


class ProductUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "core/product_update.html"
    success_url = reverse_lazy("core:product_list")
    success_message = "Sản phẩm %(name)s đã được cập nhật thành công"


class DeleteProductView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = "core/product_delete.html"
    success_url = reverse_lazy("core:product_list")
    success_message = "Sản phẩm đã được xóa thành công"


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
        if quantity == 0:
            OrderItem.objects.filter(order=order, product=product).delete()
            return

        order_item, _created = OrderItem.objects.get_or_create(
            order=order, product=product
        )
        order_item.quantity = quantity
        order_item.save()

        return order_item


class UpdateCartView(LoginRequiredMixin, View):
    def put(self, request):
        json_str = QueryDict(request.body)
        order_items = json.loads(json_str.get("cart"))
        for item in order_items.values():
            item_id = item.get("id")
            quantity = item["quantity"]
            order_item = OrderItem.objects.get(id=item_id)
            order_item.quantity = quantity
            if quantity == 0:
                order_item.delete()
            else:
                order_item.save()

        return JsonResponse({"message": "Successs"}, safe=False)

    def get(self, request):
        order, _created = Order.objects.get_or_create(
            user=request.user, state=Order.PENDING
        )

        data = {}
        for item in order.items.all():
            data[str(item.product.id)] = {"id": item.id, "quantity": item.quantity}

        return JsonResponse(data)


class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, id):
        order_item = get_object_or_404(OrderItem, pk=id)
        if order_item.order.user != request.user:
            return HttpResponse("Forbidden", status=403)

        order_item.delete()

        return redirect("core:cart_list")


class CartListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "core/cart_list.html"
    context_object_name = "order_items"

    def get_queryset(self):
        order, _created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )
        order.refresh_from_db()
        return OrderItem.objects.filter(order=order).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"], created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )

        return context


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["products"] = Product.objects.order_by("-updated_at")[:8]
        context["posts"] = Post.objects.filter(post_type=Post.BLOG).order_by(
            "-updated_at"
        )[:4]
        context["categories"] = Category.objects.all()
        return context


class ProductByCategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category).order_by("-created_at")
        paginator = Paginator(products, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"products": products, "category": category, "page_obj": page_obj}
        return render(request, "core/product_by_category.html", context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        order, _created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )
        order_items = OrderItem.objects.filter(order=order)
        form = CheckoutForm()

        context = {"order": order, "order_items": order_items, "form": form}
        return render(request, "core/checkout.html", context)

    def post(self, request):
        order, _created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                address1=form.cleaned_data["address1"],
                address2=form.cleaned_data["address2"],
                receiver=form.cleaned_data["receiver"],
                phone=form.cleaned_data["phone_number"],
            )
            address.save()
            order.address = address

            try:
                with transaction.atomic():
                    self._update_stock(order)
                    order.state = Order.VERIFY
                    order.total = order.total_price()
                    order.save()
                    return redirect("core:order_detail", pk=order.pk)
            except IntegrityError:
                self._handle_out_of_stock(order)
                order.state = Order.PENDING
                order.save()
                messages.info(request, "Sản phẩm đã hết hàng")
                return redirect("core:cart_list")
        else:
            order_items = OrderItem.objects.filter(order=order)
            context = {"order": order, "order_items": order_items, "form": form}
            return render(request, "core/checkout.html", context)

    def put(self, request):
        params = QueryDict(request.body)

        order, _created = Order.objects.get_or_create(
            user=self.request.user, state=Order.PENDING
        )
        order.delivery_fee = params.get("delivery_fee")
        order.save()

        return HttpResponse("Update success")

    def _update_stock(self, order):
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            product.quantity -= order_item.quantity
            product.save()

    def _handle_out_of_stock(self, order):
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            if product.quantity < order_item.quantity:
                order_item.quantity = product.quantity
                order_item.save()
                product.quantity = 0

            if order_item.quantity == 0:
                order_item.delete()
            product.save()


class CategoryListView(ListView):
    model = Category
    template_name = "core/categories_list.html"
    context_object_name = "categories"
    ordering = ["-updated_at"]

    def get_queryset(self) -> QuerySet[Any]:
        return Category.objects.all()


class CategoryCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "core/category_add.html"
    success_url = reverse_lazy("core:category_list")
    success_message = "Danh mục '%(label)s' đã được thêm thành công"


class CategoryUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "core/category_update.html"
    success_url = reverse_lazy("core:category_list")
    success_message = "Danh mục '%(label)s' đã được cập nhật thành công"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cate"] = self.get_object()
        return context


class CategoryDeleteView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    template_name = "core/category_delete.html"
    success_url = reverse_lazy("core:category_list")
    success_message = "Danh mục đã được xóa thành công"


class AdminOrderListView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "core/admin_order_list.html"
    context_object_name = "orders"
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["order_status"] = Order.ORDER_STATUS
        context["form"] = OrderFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        filter_type = self.request.GET.get("state")

        if filter_type is None or filter_type == "all":
            return Order.objects.all().order_by("-updated_at")

        return Order.objects.filter(state=filter_type).order_by("-updated_at")


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "core/order_list.html"
    context_object_name = "orders"
    paginate_by = 3

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .exclude(state=Order.PENDING)
            .order_by("-updated_at")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["order_status"] = Order.ORDER_STATUS
        return context


class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = "core/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        order = super().get_object(queryset)
        if order.is_deleted:
            raise Http404("Đơn hàng không tồn tại")

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = OrderItem.objects.filter(order=self.object)
        return context

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False


class OrderUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "core/order_update.html"
    success_url = reverse_lazy("core:order_list")
    success_message = "Đơn hàng đã được cập nhật thành công"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_object()
        return context


class OrderDeleteView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Order
    template_name = "core/order_delete.html"
    success_url = reverse_lazy("core:order_list")
    success_message = "Đơn hàng đã được xóa thành công"


class OrderCompletedView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if order.user != request.user:
            return HttpResponseForbidden()

        if order.state == Order.DELIVERY:
            order.state = Order.COMPLETED
            order.save()
            messages.success(request, "Đơn hàng đã được hoàn thành")
            return redirect("core:order_list")
        else:
            messages.success(request, "Đơn hàng chưa được giao, không thể hoàn thành")
            return redirect("core:order_list")


class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if order.user != request.user:
            return HttpResponseForbidden()

        if order.state == Order.VERIFY:
            order.state = Order.CANCEL
            order.save()
            messages.success(request, "Đơn hàng đã được hủy")
            return redirect("core:order_detail", pk=order.pk)
        else:
            return redirect("core:order_detail", pk=order.pk)


def category_product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, "core/product_category.html", context)


class BugReportView(View):
    def get(self, request):
        form = BugReportForm()
        return render(request, "core/bug_report.html", {"form": form})

    def post(self, request):
        form = BugReportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = Post.BUG_REPORT
            post.save()
            messages.success(request, "Cảm ơn bạn đã gửi báo cáo")
            return redirect("core:home")
        else:
            return render(request, "core/bug_report.html", {"form": form})
