from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.models import Category

from .forms import PostForm
from .models import Post

# Create your views here.


class ListPostView(ListView):
    model = Post
    paginate_by = 8
    ordering = "-updated_at"
    template_name = "blog/posts_list.html"
    context_object_name = "posts_list"

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.BLOG)


class BugReportListView(ListView):
    model = Post
    paginate_by = 8
    ordering = "-updated_at"
    template_name = "core/bug_list.html"
    context_object_name = "bug_list"

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.BUG_REPORT)


class AddPostView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_new.html"
    success_url = reverse_lazy("blog:list_posts")
    success_message = "Thêm bài viết thành công!"


class UpdatePostView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy("blog:list_posts")
    success_message = "Cập nhật bài viết thành công!"


class DeletePostView(SuccessMessageMixin, View):
    model = Post
    form_class = PostForm
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:list_posts")
    success_message = "Xóa bài viết thành công!"

    def post(self, request, pk: int):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        messages.success(request, self.success_message)
        return redirect("blog:list_posts")


class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.get(pk=self.kwargs["pk"])
        context["categories"] = Category.objects.all()
        return context
