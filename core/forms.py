from django import forms

from .models import Product


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


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(initial=1)
