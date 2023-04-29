from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "quantity", "summary", "thumbnail"]

        labels = {
            "name": "Tên cây",
            "price": "Giá",
            "summary": "Thông tin về cây",
            "thumbnail": "Ảnh sản phẩm",
            "category": "Danh mục",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "text-input"}),
            "price": forms.TextInput(attrs={"class": "text-input"}),
            "summary": forms.Textarea(attrs={"class": "text-area-input text-input"}),
            "thumbnail": forms.FileInput(attrs={"class": "file-input"}),
        }


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(initial=1)
