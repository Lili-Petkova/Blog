from django.urls import path

from . import views
from .views import post_with_comment, start, user_posts


app_name = 'catalog'
urlpatterns = [
    path('', start, name='start'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
    path('create_post/', views.PostCreateView.as_view(), name='create_post'),
    path('update_post/<int:pk>/', views.PostUpdateView.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('own_posts/', views.OwnPostsListView.as_view(), name='own_posts'),
    path('all_posts/', views.AllPostsListView.as_view(), name='all_posts'),
    path('post/<int:pk>/', post_with_comment, name='one_post'),
    path('user_posts/<int:pk>/', user_posts, name='user_posts')
]
