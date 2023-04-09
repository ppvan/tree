from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import (ProfileForm, UserAuthenticationForm, UserRegisterForm,
                    UserUpdateForm)
from .tokens import account_activation_token

# Create your views here.


def test_view(request):

    messages.info(request, 'This is a test message 1')
    messages.success(request, 'This is a test message 2')
    messages.warning(request, 'This is a test message 3')
    messages.error(request, 'This is a test message 4')
    return render(request, 'test.html')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)

        return render(request, 'user/profile.html', {'u_form': u_form, 'p_form': p_form})

    def post(self, request):
        profile = request.user.profile
        u_form = UserUpdateForm(request.POST, instance=request.user)

        print(request.user.email)

        p_form = ProfileForm(request.POST, request.FILES, instance=profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        if not (u_form.is_valid() and p_form.is_valid()):
            return render(request, 'user/profile.html', context)

        u_form.save()
        p_form.save()

        messages.success(request, 'Cập nhật thành công')
        return redirect('profile')


class UserLoginView(auth_views.LoginView):
    template_name = 'user/login.html'
    next_page = 'home'
    authentication_form = UserAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'Chào mừng {user}')
        return super().form_valid(form)


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'user/register.html', {'form': form})

        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self._send_activation_email(request, user)
        messages.success(request, 'Kiểm tra email để kích hoạt tài khoản')
        return redirect('home')

    def _send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Kích hoạt tài khoản của bạn'
        message = render_to_string('user/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
    pass


class UserActivateView(View):
    def get(self, request, uidb64, token):
        user = self._decode_user(uidb64, token)
        if user:
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Activation link is invalid!')

    def _decode_user(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return user if user and account_activation_token.check_token(user, token) else None


class UserPasswordReset(auth_views.PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_email.html'


class UserPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class UserPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'
