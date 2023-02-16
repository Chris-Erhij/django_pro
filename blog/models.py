from typing import List, Tuple
from django.db import models
from django.utils import timezone
from django.db.models import (
    Model, CharField, SlugField, TextField, DateTimeField, Index
)


class Post(Model):
    class Status(models.TextChoices):
        DRAFT: Tuple[str] = ('PB', 'Published')
        PUBLISHED: Tuple[str] = ('DT', 'Draft')

    blog_title: CharField = models.CharField("title", max_length=250)
    slug: SlugField = models.SlugField(max_length=250)
    body: TextField = models.TextField()
    date_published: DateTimeField = models.DateTimeField(default=timezone.now)
    date_created: DateTimeField = models.DateTimeField(auto_now_add=True)
    date_modified: DateTimeField = models.DateTimeField(auto_now=True)
    status: CharField = models.CharField(max_length=2,
                                         choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering: List[str] = ['-date_published', ]  # in reverse order
        indexes: List[Index] = [models.Index(fields=['-date_published', ])]

    def __str__(self) -> str | CharField:
        return self.blog_title
