from django.shortcuts import render
from django.http import Http404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, PublishedManager


def post_list(request: HttpRequest) -> HttpResponse:
    posts: PublishedManager  = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})
