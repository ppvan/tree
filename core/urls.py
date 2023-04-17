from django.urls import path

from .views import AddItemView, delete_item, list_item, update_item

app_name = 'core'
urlpatterns = [
    path('add-product/', AddItemView.as_view(), name='add_item'),
    path('list-product/', list_item, name='list_item'),
    path('delete-product/<int:pk>', delete_item, name='delete_item'),
    path('update-product/<int:pk>', update_item, name='update_item'),
]
