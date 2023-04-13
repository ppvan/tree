from django.urls import path
from .views import item_list,Add_item


app_name='core'
urlpatterns = [
    path('add-product/' ,Add_item.as_view() ,name='add_item'),
]