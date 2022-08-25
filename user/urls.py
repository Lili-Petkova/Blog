from django.urls import path

from user.views import RegisterFormView, UserProfile, UpdateProfile, UserLogoutView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
