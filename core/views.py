from django.shortcuts import HttpResponse, redirect, render
from django.views import View

from .forms import ProductForm
from .models import Product


# Create your views here.
def item_list(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "item_list.html", context)


class AddItemView(View):
    def get(self, request):
        p = ProductForm()
        context = {'pr': p}
        return render(request, "add_item.html", context)

    def post(self, request):
        p = ProductForm(request.POST)
        if not p.is_valid():
            return HttpResponse("ban nhap sai du lieu")
        p.save()
        return HttpResponse("da them san pham")


def list_item(request):
    p = Product.objects.all()
    context = {'products': p}
    return render(request, 'list_item.html', context)


def delete_item(request, pk):
    p = Product.objects.get(id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('/core/list-item/')
    return render(request, 'delete_item.html', {'pr': p})


def update_item(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/core/list-item/')
    context = {'form': form}
    return render(request, 'update_item.html', context)
