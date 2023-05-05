from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms

from .models import Address, Category, District, Product, Province, Ward


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


class CheckoutForm(forms.Form):
    phone = forms.CharField(max_length=255, label="Số điện thoại")

    receiver = forms.CharField(max_length=255, label="Người nhận")

    province = forms.ChoiceField(
        choices=[(0, "Chọn tỉnh/thành phố")], label="Tỉnh/thành phố"
    )

    district = forms.ChoiceField(choices=[(0, "Chọn quận/huyện")], label="Quận/huyện")

    ward = forms.ChoiceField(choices=[(0, "Chọn phường/xã")], label="Phường/xã")

    address = forms.CharField(max_length=255, label="Địa chỉ")

    note = forms.CharField(
        max_length=255, required=False, widget=forms.Textarea, label="Ghi chú"
    )

    transport = forms.ChoiceField(
        choices=[(0, "Chọn phương thức vận chuyển")], label=""
    )
