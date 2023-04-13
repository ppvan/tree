from django.forms import ModelForm
from .models import Product
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','summary' ]

        labels = {
            'name': 'Tên hoa',
            'price': 'giá',
            'summary': 'thông tin về hoa'
          
                }

        help_texts = {
           
        }

