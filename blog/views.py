from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
# Create your views here.


def index(request):
    return render(request, 'blog/index.html', {'posts': Post.objects.all()})


def get(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})


def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('blog:get', pk=post.pk)
        else:
            # print(form.errors)
            return HttpResponse(f"{form.errors}")
    else:
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})


def update(request, pk: int):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('blog:get', pk=post.pk)
        else:
            # print(form.errors)
            return HttpResponse(f"{form.errors}")
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_update.html', {'form': form, 'id': pk})


def delete(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:index')
