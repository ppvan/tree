from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView

from .forms import (
    ProfileForm,
    UserAuthenticationForm,
    UserPasswordResetForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .tokens import account_activation_token

# Create your views here.


def test_view(request):
    messages.info(request, "This is a test message 1")
    messages.success(request, "This is a test message 2")
    messages.warning(request, "This is a test message 3")
    messages.error(request, "This is a test message 4")
    return render(request, "test.html")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)

        return render(
            request, "user/profile.html", {"u_form": u_form, "p_form": p_form}
        )

    def post(self, request):
        profile = request.user.profile
        u_form = UserUpdateForm(request.POST, instance=request.user)

        p_form = ProfileForm(request.POST, request.FILES, instance=profile)

        context = {"u_form": u_form, "p_form": p_form}

        if not (u_form.is_valid() and p_form.is_valid()):
            return render(request, "user/profile.html", context)

        u_form.save()
        p_form.save()

        messages.success(request, "Cập nhật thành công")
        return redirect("profile")


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "user/login.html"
    next_page = "core:home"
    authentication_form = UserAuthenticationForm
    success_message = "Đăng nhập thành công"


class UserRegisterView(SuccessMessageMixin, CreateView):
    success_message = "Đăng ký thành công, Hãy kiểm tra email để kích hoạt tài khoản"
    success_url = reverse_lazy("core:home")
    template_name = "user/register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self._send_activation_email(self.request, user)
        return super().form_valid(form)

    # def post(self, request):
    #     form = UserRegisterForm(request.POST)

    #     if not form.is_valid():
    #         return render(request, "user/register.html", {"form": form})

    #     user = form.save(commit=False)
    #     user.is_active = False
    #     user.save()
    #     self._send_activation_email(request, user)
    #     return redirect("core:home")

    def _send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = "Kích hoạt tài khoản của bạn"
        message = render_to_string(
            "user/activation_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        user.email_user(subject, message)


class UserActivateView(View):
    def get(self, request, uidb64, token):
        user = self._decode_user(uidb64, token)
        if user:
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            group = Group.objects.get(name="Customers")
            user.groups.add(group)
            login(request, user)
            return redirect("core:home")
        else:
            return HttpResponse("Liên kết kích hoạt không hợp lệ")

    def _decode_user(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return (
            user if user and account_activation_token.check_token(user, token) else None
        )


class UserPasswordReset(SuccessMessageMixin, auth_views.PasswordResetView):
    template_name = "user/password_reset.html"
    email_template_name = "user/password_reset_email.html"
    success_message = "Hãy kiểm tra email để lấy lại mật khẩu"
    success_url = reverse_lazy("password_reset_done")
    form_class = UserPasswordResetForm


class UserPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = "user/password_reset_done.html"


class UserPasswordResetConfirm(
    SuccessMessageMixin, auth_views.PasswordResetConfirmView
):
    template_name = "user/password_reset_confirm.html"
    labels = {"new_password1": "Mật khẩu mới", "new_password2": "Nhập lại mật khẩu mới"}
    success_message = "Đổi mật khẩu thành công"
    success_url = reverse_lazy("login")
