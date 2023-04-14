from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'summary']

        labels = {
            'name': 'Tên hoa',
            'price': 'Giá',
            'summary': 'Thông tin về hoa'

        }

        help_texts = {

        }
