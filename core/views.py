from django.shortcuts import render,HttpResponse
from .models import Product
from django.views import View
from .forms import ProductForm

# Create your views here.
def item_list(request):
    context={
        'items':Product.objects.all()
    }
    return render(request,"item_list.html",context)

class Add_item(View):
    def get(self,request):
        p = ProductForm()
        context ={'pr':p}
        return render(request,"add_item.html",context)
    def post(self,request):
        p = ProductForm(request.POST)
        if not p.is_valid():
            return HttpResponse("ban nhap sai du lieu")
        p.save()
        return HttpResponse("da them san pham")
        
