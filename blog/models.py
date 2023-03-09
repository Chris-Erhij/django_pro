from typing import List, Tuple, Any
from django.db import models
from django.utils import timezone
from django.db.models import (
    Model, CharField, SlugField, TextField, DateTimeField, Index, ForeignKey,
    Manager
)
from django.contrib.auth.models import User


class PublishedManager(models.Manager):  # Overriding manager class
    def get_queryset(self) -> Any:
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(Model):
    class Status(models.TextChoices):
        DRAFT: Tuple[str] = ('PB', 'Published') # type: ignore
        PUBLISHED: Tuple[str] = ('DT', 'Draft') # type: ignore

    blog_title: CharField = models.CharField("title", max_length=250)
    slug: SlugField = models.SlugField(max_length=250)
    author: ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts',
    )
    body: TextField = models.TextField()
    date_published: DateTimeField = models.DateTimeField(default=timezone.now)
    date_created: DateTimeField = models.DateTimeField(auto_now_add=True)
    date_modified: DateTimeField = models.DateTimeField(auto_now=True)
    status: CharField = models.CharField(max_length=2,
                                         choices=Status.choices, default=Status.DRAFT)

    objects: Manager = models.Manager()  # Default query manager
    published: PublishedManager = PublishedManager()  # Custom query manager

    class Meta:
        ordering: List[str] = ['-date_published', ]  # in reverse order
        indexes: List[Index] = [models.Index(fields=['-date_published', ])]

    def __str__(self) -> str | CharField:
        return self.blog_title
