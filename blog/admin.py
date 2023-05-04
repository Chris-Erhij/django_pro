from django.contrib import admin
from .models import Post, Comment
import typing as ty

admin.site.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: ty.List[str,] = [
        'name', 'email', 'created', 'updated', 'active',
    ]
    list_filter: ty.List[str,] = ['active', 'created', 'updated',]
    search_fields: ty.List[str,] = ['name', 'email', 'body']
    