from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Tài khoản'
        self.fields['username'].help_text = 'Ngắn hơn 150 ký tự. Chỉ chứa chữ cái, số và @/./+/-/_'

        self.fields['email'].label = 'Email'

        self.fields['password1'].help_text = 'Ít nhất 8 ký tự. Đầy đủ các ký tự chữ và số.'
        self.fields['password1'].label = 'Mật khẩu'

        self.fields['password2'].label = 'Nhập lại mật khẩu'
        self.fields['password2'].help_text = 'Mật khẩu y như cũ (để xác nhận)'

        self.error_messages['invalid_login'] = 'Mật khẩu hoặc tài khoản không đúng'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Tài khoản'
        self.fields['password'].label = 'Mật khẩu'
        self.error_messages['invalid_login'] = 'Mật khẩu hoặc tài khoản không đúng'

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Tài khoản',
            'password': 'Mật khẩu'
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
