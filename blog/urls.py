from django.urls import path
from . import views

app_name: str = 'blog'  # URL namespacing
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id/>', views.post_detail, name='post_detail'),
]  # Map URL patterns to views using the path() function. In this case just two.
