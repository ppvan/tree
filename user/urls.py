from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.get, name='get'),
    path('register/', views.register, name='register'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
