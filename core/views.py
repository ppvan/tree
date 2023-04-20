from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Product


class AddProductView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'summary']
    template_name = 'core/product_new.html'
    success_url = reverse_lazy('core:list_product')
    success_message = "Sản phẩm %(name)s được thêm thành công"


class ListProductView(ListView):
    model = Product
    template_name = 'core/products_list.html'
    context_object_name = 'products_list'


class DetailProductView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'price', 'summary']
    template_name = 'core/product_update.html'
    success_url = reverse_lazy('core:list_product')


class DeleteProductView(DeleteView):
    model = Product
