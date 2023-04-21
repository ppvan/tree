from django import forms

from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "summary",
            "thumbnail",
        ]

        labels = {
            "name": "Tên hoa",
            "price": "Giá",
            "summary": "Thông tin về hoa",
            "thumbnail": "Ảnh chính",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "text-input"}),
            "price": forms.TextInput(attrs={"class": "text-input"}),
            "summary": forms.Textarea(attrs={"class": "text-area-input text-input"}),
            "thumbnail": forms.FileInput(attrs={"class": "file-input"}),
        }


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "file-input", "multiple": True})
    )

    class Meta:
        model = ProductImage
        fields = [
            "image",
        ]
        labels = {
            "image": "Ảnh phụ",
        }
