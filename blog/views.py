from django.shortcuts import render
from django.http import Http404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, PublishedManager
from django.core.paginator import (
    Paginator, PageNotAnInteger, EmptyPage,
)


def post_list(request: HttpRequest) -> HttpResponse:
    """Return a list of the most recently published post
    """
    post_list: PublishedManager = Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)  # type: ignore
    except EmptyPage:
        # If page number is out of rage, deliver the last page.
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if page number is not an integer, deliver the first page.
        posts = paginator.page(1)

    return render(request, 'blog/post/list.html', {'posts': posts})

# Modified for SEO friendliness
def post_detail(request: HttpRequest, year: str, month: str, day: str, post: str) -> HttpResponse:
    """Return an SEO friendly URL of a Post model object.

        I.e. An httpresponse of the detail of a specific post using a combination of
        it's date published and slug.
    """
    try:
        post_context: Post = Post.published.get(status=Post.Status.PUBLISHED,
                                                date_published__year=year, date_published__month=month,
                                                date_published__day=day, slug=post
                                                )
    except Post.DoesNotExist:
        raise Http404("post not found") from None
    return render(request, 'blog/post/detail.html', {'post_context': post_context})
