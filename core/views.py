from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm, ProductImageForm
from .models import Product, ProductImage


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


class AddProductView(
    LoginRequiredMixin, PageTitleViewMixin, SuccessMessageMixin, CreateView
):
    model = Product
    form_class = ProductForm

    title = "Thêm sản phẩm"
    template_name = "core/product_new.html"
    success_url = reverse_lazy("core:list_product")
    success_message = "Sản phẩm %(name)s được thêm thành công"


class ListProductView(ListView):
    model = Product
    template_name = "core/products_list.html"
    context_object_name = "products_list"


class DetailProductView(DetailView):
    model = Product
    template_name = "core/product_detail.html"


class UpdateProductView(UpdateView):
    model = Product
    fields = ["name", "price", "summary"]
    template_name = "core/product_update.html"
    success_url = reverse_lazy("core:list_product")


class DeleteProductView(DeleteView):
    model = Product


# admin
def list_product(request):
    p = Product.objects.all()
    context = {"products": p}
    return render(request, "administrator/list_product.html", context)


def delete_product(request, pk):
    p = Product.objects.get(id=pk)
    if request.method == "POST":
        p.delete()
        return redirect("/core/list-product/")
    return render(request, "administrator/delete_product.html", {"pr": p})


def list_catagory(request):
    return render(request, "administrator/list_catagory.html")


def list_post(request):
    return render(request, "administrator/list_post.html")


def add_product(request):
    p = ProductForm()
    i = ProductImageForm()
    if request.method == "POST":
        i = ProductImageForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        p = ProductForm(request.POST, request.FILES)
        if not p.is_valid():
            return HttpResponse("ban nhap sai du lieu")
        product = p.save()
        for file in files:
            ProductImage.objects.create(product=product, image=file)

        return HttpResponse("da them san pham")

    context = {"pro_form": p, "img_form": i}
    return render(request, "administrator/add_product.html", context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    img_form = ProductImageForm()
    pro_form = ProductForm(instance=product)
    if request.method == "POST":
        pro_form = ProductForm(request.POST, request.FILES, instance=product)
        img_form = ProductImageForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        if pro_form.is_valid():
            product = pro_form.save()
            for file in files:
                ProductImage.objects.create(product=product, image=file)
            return redirect("/core/list-product/")
    context = {"pro_form": pro_form, "img_form": img_form}
    return render(request, "administrator/update_product.html", context)
