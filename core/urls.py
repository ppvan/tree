from django.urls import path
from .views import list_item,Add_item,delete_item,update_item


app_name='core'
urlpatterns = [
    path('add-product/' ,Add_item.as_view() ,name='add_item'),
    path('list-product/' ,list_item ,name='list_item'),
    path('delete-product/<str:pk>' ,delete_item ,name='delete_item'),
    path('update-product/<str:pk>',update_item,name='update_item'),
]