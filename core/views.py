from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ProductForm
from .models import Category, Product


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
    template_name = "core/product_new.html"
    success_url = reverse_lazy("core:list_product")
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


class CategoryProductView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {"products": products, "categories": categories}
        return render(request, "core/product_category.html", context)


def add_to_cart(request):
    cart_p = {}
    cart_p[str(request.GET['id'])]= {
        'name':request.GET['name'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data':request.session['cartdata'], 'totalitems':len(request.session['cartdata'])})


def cart_list(request):
    total = 0;
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {'cart_data':request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'total_price':total})
    return render(request, "core/cart.html", {'cart_data':'', 'totalitems':0, 'total_price':total})

def delete_cart_item(request):
    p_id = request.GET['id']
    if 'cartdata' in request.session:
            if p_id in request.session['cartdata']:
                cart_data = request.session['cartdata']
                del request.session['cartdata'][p_id]
                request.session['cartdata'] = cart_data
    total = 0
    for p_id,item in request.session['cartdata'].items():
            total += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',{'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_price': total})
    return JsonResponse({'data': t,'totalitems': len(request.session['cartdata'])})
	

def update_cart_item(request):
    p_id = request.GET['id']
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
            if p_id in request.session['cartdata']:
                cart_data = request.session['cartdata']
                cart_data[str(request.GET['id'])]['qty'] = p_qty;
                request.session['cartdata'] = cart_data
    total = 0
    for p_id,item in request.session['cartdata'].items():
            total += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',{'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_price': total})
    return JsonResponse({'data': t,'totalitems': len(request.session['cartdata'])})
	

