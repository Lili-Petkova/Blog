from catalog import views
from catalog.views import contact, create_post, delete_post, post_with_comment, start, update_post, user_posts

from django.urls import path


app_name = 'catalog'
urlpatterns = [
    path('', start, name='start'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
    path('create_post/', create_post, name='create_post'),
    path('update_post/<int:pk>/', update_post, name='update_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
    path('own_posts/', views.OwnPostsListView.as_view(), name='own_posts'),
    path('all_posts/', views.AllPostsListView.as_view(), name='all_posts'),
    path('post/<int:pk>/', post_with_comment, name='one_post'),
    path('user_posts/<int:pk>/', user_posts, name='user_posts'),
    path('contact/', contact, name='contact')
]
