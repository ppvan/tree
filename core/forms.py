from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "thumbnail",
            "category",
            "price",
            "quantity",
            "summary",
            "description",
        ]

        labels = {
            "name": "Tên cây",
            "price": "Giá",
            "summary": "Thông tin",
            "thumbnail": "Ảnh sản phẩm",
            "category": "Danh mục",
            "quantity": "Số lượng",
            "description": "Mô tả chi tiết",
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["label", "image"]

        labels = {"label": "Tên danh mục", "image": "Ảnh mô tả"}


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(initial=1)
