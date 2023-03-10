from django.shortcuts import render
from django.http import Http404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, PublishedManager


def post_list(request: HttpRequest) -> HttpResponse:
    posts: PublishedManager  = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    try:
        post: PublishedManager = Post.published.get(id=id)
    except Post.DoesNotExit as e:
        raise Http404("Post not found") from e
    return render(request, 'blog/post/detail.html', {'post': post})

