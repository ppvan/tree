import re

from django import forms

from blog.models import Post

from .models import Category, Order, Product


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


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["label", "image"]

        labels = {"label": "Tên danh mục", "image": "Ảnh mô tả"}


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(initial=1)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["state"]


class CheckoutForm(forms.Form):
    phone_number = forms.CharField(max_length=255, label="Số điện thoại")
    receiver = forms.CharField(max_length=255, label="Người nhận")
    province = ChoiceFieldNoValidation(
        choices=[(0, "Chọn tỉnh/thành phố")],
        label="Tỉnh/thành phố",
        validators=[],
    )
    district = ChoiceFieldNoValidation(
        choices=[(0, "Chọn quận/huyện")], label="Quận/huyện"
    )
    ward = ChoiceFieldNoValidation(choices=[(0, "Chọn phường/xã")], label="Phường/xã")
    address2 = forms.CharField(
        max_length=255,
        label="Địa chỉ chi tiết",
        widget=forms.TextInput(attrs={"placeholder": "Số nhà, tên đường, ..."}),
    )
    address1 = forms.CharField(
        max_length=255,
        label="Địa chỉ",
        widget=forms.TextInput(
            attrs={
                "readonly": True,
                "placeholder": "Tỉnh/thành phố, Quận/huyện, Phường/xã",
            }
        ),
    )
    note = forms.CharField(
        max_length=255, required=False, widget=forms.Textarea, label="Ghi chú"
    )
    transport = ChoiceFieldNoValidation(
        choices=[(0, "Chọn phương thức vận chuyển")], label=""
    )

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if not re.match(r"^[0-9]{10}$", data):
            raise forms.ValidationError("Số điện thoại không hợp lệ")
        return data


class OrderFilterForm(forms.Form):
    FILTER_STATE = [("all", "Tất cả")] + Order.ORDER_STATUS

    state = forms.ChoiceField(
        label="",
        choices=FILTER_STATE,
        required=False,
        widget=forms.Select(attrs={"class": "mt-3"}),
    )


class BugReportForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "cover_image", "content"]

        widgets = {
            "content": forms.Textarea(attrs={"cols": 60}),
        }
