from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import UserAuthenticationForm, UserRegisterForm
from .tokens import account_activation_token

# Create your views here.


class UserLoginView(auth_views.LoginView):
    template_name = 'user/login.html'
    next_page = 'home'
    authentication_form = UserAuthenticationForm


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

        return redirect('home')

    def _send_activation_email(request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('user/account_activation_email.html', {
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

    def _decode_user(uidb64, token):
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
