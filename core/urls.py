from django.urls import path

from .views import (
    AddItemView, delete_item, list_item, update_item,list_product,delete_product,list_catagory,list_post,add_product,update_product)

app_name = 'core'
urlpatterns = [
    path('list-product/',list_product,name='list_product'),
    path('delete-product/<int:pk>', delete_product, name='delete_product'),
    path('list-catagory/',list_catagory,name='list_catagory'),
    path('list-post/',list_post,name='list_post'),
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:pk>', update_product, name='update_product'),
]
