from django.shortcuts import HttpResponse, redirect, render
from django.views import View

from .forms import ProductForm,ProductImageForm
from .models import Product,ProductImage


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


# admin
def list_product(request):
    p = Product.objects.all()
    context = {'products': p}
    return render(request,'administrator/list_product.html',context)

def delete_product(request, pk):
    p = Product.objects.get(id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('/core/list-product/')
    return render(request, 'administrator/delete_product.html', {'pr': p})


def list_catagory(request):
    return render(request,'administrator/list_catagory.html')


def list_post(request):
    return render(request,'administrator/list_post.html')


def add_product(request):
    p = ProductForm()
    i = ProductImageForm()
    if request.method == "POST":
        i = ProductImageForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        p = ProductForm(request.POST, request.FILES)
        if not p.is_valid():
            return HttpResponse("ban nhap sai du lieu")
        product=p.save()
        for file in files: 
            ProductImage.objects.create(product=product, image=file)

        return HttpResponse("da them san pham")
    
    context = {'pro_form': p, 'img_form': i}
    return render(request, "administrator/add_product.html", context)
    

def update_product(request, pk):
    product = Product.objects.get(id=pk)
    img_form = ProductImageForm()
    pro_form = ProductForm(instance=product)
    if request.method == 'POST':
        pro_form = ProductForm(request.POST,request.FILES, instance=product)
        img_form = ProductImageForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        if pro_form.is_valid():
            product=pro_form.save()
            for file in files: 
                ProductImage.objects.create(product=product, image=file)
            return redirect('/core/list-product/')
    context = {'pro_form': pro_form, 'img_form': img_form}
    return render(request, 'administrator/update_product.html', context)
