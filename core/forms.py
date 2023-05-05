from django import forms

from .models import Address, Category, Product


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


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["phone", "receiver", "address1", "address2"]

        labels = {
            "address1": "Địa chỉ",
            "address2": "Chi tiết",
            "receiver": "Người nhận",
            "phone": "Số điện thoại",
        }

        widgets = {
            "address1": forms.TextInput(attrs={"placeholder": "Tỉnh, Thành phố"}),
            "address2": forms.TextInput(attrs={"placeholder": "Số nhà, tên đường"}),
        }
