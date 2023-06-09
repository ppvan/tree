from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # Work around cus password1 and password2 are not fields
        self.fields["password1"].help_text = ""
        self.fields["password1"].label = "Mật khẩu"

        self.fields["password2"].label = "Nhập lại mật khẩu"
        self.fields["password2"].help_text = "Mật khẩu y như cũ (để xác nhận)"

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

        labels = {
            "username": "Tài khoản",
            "email": "Email",
            "first_name": "Họ",
            "last_name": "Tên",
        }

        help_texts = {
            "username": "Ngắn hơn 150 ký tự. Chỉ chứa chữ cái, số và @/./+/-/_",
            "email": "Địa chỉ email hợp lệ",
            "first_name": "Ngắn hơn 150 ký tự",
            "last_name": "Ngắn hơn 30 ký tự",
        }

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email đã được sử dụng")
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]

        labels = {"avatar": "Ảnh đại diện", "bio": "Giới thiệu"}


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "Email"

    class Meta:
        model = User
        fields = ["email"]


class UserPasswordResetConfirmForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Mật khẩu không trùng nhau",
    }

    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Mật khẩu phải có ít nhất 8 ký tự và không được trùng với mật khẩu cũ",
    )
    new_password2 = forms.CharField(
        label="Mật khẩu mới (xác nhận)",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Tài khoản"
        self.fields["password"].label = "Mật khẩu"
        self.error_messages["invalid_login"] = "Mật khẩu hoặc tài khoản không đúng"

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {"username": "Tài khoản", "password": "Mật khẩu"}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

        labels = {
            "username": "Tài khoản",
            "first_name": "Họ",
            "last_name": "Tên",
        }
