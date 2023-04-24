from django.urls import path

from .views import (
    AddPostView,
    DeletePostView,
    ListPostView,
    PostDetailView,
    UpdatePostView,
)

app_name = "blog"

urlpatterns = [
    path("list/", ListPostView.as_view(), name="list_posts"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("new/", AddPostView.as_view(), name="new"),
    path("<int:pk>/update/", UpdatePostView.as_view(), name="update"),
    path("<int:pk>/delete/", DeletePostView.as_view(), name="delete"),
]
