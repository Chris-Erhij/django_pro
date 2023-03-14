from typing import List, Any
from django.db import models
from django.utils import timezone
from django.db.models import (
    Model, CharField, SlugField, TextField, DateTimeField, Index, ForeignKey,
    Manager,
)
from django.contrib.auth.models import User
from django.urls import reverse


# Custom object mangager class
class PublishedManager(models.Manager):  # Overriding manager class
    def get_queryset(self) -> Any:
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)  # Overridden super get_query() of the Manager class.


class DraftedManager(models.Manager):
     def get_queryset(self) -> Any:
          return super().get_queryset().filter(status=Post.Status.DRAFT)


class Post(Model):
    class Status(models.TextChoices):
        """Enum class for blog_post choices
        
        Best defined in the model for easy usage from anywhere in the code
        """
        PUBLISHED = ('PB', 'Published')  # Name, value, and lable repectively
        DRAFT = ('DT', 'Draft')

    blog_title: CharField = models.CharField("title", max_length=250)
    slug: SlugField = models.SlugField(
        max_length=250,
        unique_for_date='date_published'  # For SEO friendly URLs for posts, using unique slugs for date published
    )
    author: ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts',
    )  # A many-to-one relationship

    body: TextField = models.TextField()
    date_published: DateTimeField = models.DateTimeField(default=timezone.now)
    date_created: DateTimeField = models.DateTimeField(auto_now_add=True)
    date_modified: DateTimeField = models.DateTimeField(auto_now=True)
    status: CharField = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    objects: Manager = models.Manager()  # Default query manager
    published: PublishedManager = PublishedManager()  # Custom query manager
    drafted: DraftedManager = DraftedManager()

    class Meta:
        ordering: List[str] = ['-date_published', ]  # in reverse order
        indexes: List[Index] = [models.Index(fields=['-date_published', ])]

    def __str__(self) -> CharField | str:
        return self.blog_title

    def get_absolute_url(self) -> str:
         """Return a canonical URL dynamically.

            I.e. The main URL or details page of a specific model object.
         """
         return reverse('blog:post_detail', args=(self.date_published.year, self.date_published.month,
                                                  self.date_published.day, self.slug
                                                  ))  # SEO
    