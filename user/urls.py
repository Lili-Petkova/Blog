from user.views import RegisterFormView, UpdateProfile, UserLogoutView, UserProfile

from django.urls import path

app_name = 'user'
urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
