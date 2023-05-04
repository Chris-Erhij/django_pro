from django.forms import Form, ModelForm
from django import forms
from .models import Comment
import typing as ty


class EmailPostForm(Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(ModelForm):
    model = Comment
    fields: ty.List[str,] = ['name', 'email', 'body']
    