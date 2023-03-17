from django.urls import path
from . import views

app_name: str = 'blog'  # URL namespacing
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),  # For SEO friendly post URL
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]  # Map URL patterns to views using the path() function. In this case just two.
