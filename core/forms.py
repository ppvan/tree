from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "summary"]

        labels = {"name": "Tên sản phẩm", "price": "Mệnh giá", "summary": "Mô tả"}

        help_texts = {}
