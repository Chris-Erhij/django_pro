from django.shortcuts import render
from django.http import Http404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, PublishedManager
# from django.shortcuts import get_object_or_404


def post_list(request: HttpRequest) -> HttpResponse:
    posts: PublishedManager = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

# Modified for SEO friendliness
def post_detail(request: HttpRequest, year: str, month: str, day: str, post: str) -> HttpResponse:
    try:
        post_context: Post = Post.published.get(status=Post.Status.PUBLISHED,
                                                date_published__year=year, date_published__month=month,
                                                date_published__day=day, slug=post
                                                )
    except Post.DoesNotExist:
        raise Http404("post not found") from None
    return render(request, 'blog/post/detail.html', {'post_context': post_context})
