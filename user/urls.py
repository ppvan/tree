from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('activate_account/<uidb64>/<token>/',
         views.UserActivateView.as_view(), name='activate_account'),
    # path('activate_account_sent', , name='activate_account_sent'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
