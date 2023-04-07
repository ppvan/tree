from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

# app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # Password change
    path('password-change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Password reset
    path('password-reset/', views.UserPasswordReset.as_view(), name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetDone.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # Activate account
    path('activate_account/<uidb64>/<token>/', views.UserActivateView.as_view(),
         name='activate_account'),
    path('activate_account_sent', views.UserActivateView.as_view(), name='activate_account_sent'),
]
