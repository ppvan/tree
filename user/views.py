from django.shortcuts import redirect, render

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.


class UserLoginView(auth_views.LoginView):
    template_name = 'user/user_login.html'

    pass


def index(request):
    users = User.objects.all()
    return render(request, 'user/index.html', {'users': users})


@login_required
def get(request, pk: int):
    return HttpResponse(f"get {pk}")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form.save()
        return redirect('user:index')
    else:
        form = UserRegisterForm()

        return render(request, 'user/user_register.html', {'form': form})


def update(request, pk: int):

    current_user = User.objects.get(pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=current_user)
        form.save()
        return redirect('user:index')
    else:
        form = UserUpdateForm(instance=current_user)

        return render(request, 'user/user_update.html', {'form': form})
    return HttpResponse(f"update {pk}")


def delete(request, pk: int):
    return HttpResponse(f"delete {pk}")
