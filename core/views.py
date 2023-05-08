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
    TemplateView,
    UpdateView,
)

from blog.models import Post

from .forms import AddToCartForm, CategoryForm, CheckoutForm, ProductForm
from .models import Address, Category, Order, OrderItem, Product, Ward


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
    ordering = ["-updated_at"]
    paginate_by = 50


class DetailProductView(DetailView):
    model = Product
    template_name = "core/product_detail.html"

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


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["products"] = Product.objects.order_by("-created_at")[:8]
        context["posts"] = Post.objects.order_by("-updated_at")[:4]
        context["categories"] = Category.objects.all()
        return context


class ProductByCategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        context = {"products": products, "category": category}
        return render(request, "home.html", context)


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
            ward = get_object_or_404(Ward, pk=form.cleaned_data["ward"])
            address = Address.objects.create(
                address=form.cleaned_data["address"],
                receiver=form.cleaned_data["receiver"],
                phone=form.cleaned_data["phone"],
                ward=ward,
                order=order,
            )
            address.save()
            order.address = address
            order.state = Order.DELIVERY
            order.save()
            return redirect("core:home")
        else:
            order_items = OrderItem.objects.filter(order=order)
            context = {"order": order, "order_items": order_items, "form": form}
            return render(request, "core/checkout.html", context)


class CategoryListView(ListView):
    model = Category
    template_name = "core/categories_list.html"
    context_object_name = "categories"
    ordering = ["-updated_at"]


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


def category_product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, "core/product_category.html", context)
