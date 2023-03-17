from django.forms import Form, ModelForm
from django import forms


class EmailPostForm(Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(ModelForm):
    pass
