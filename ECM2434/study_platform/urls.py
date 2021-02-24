from django.urls import path
from . import views
from . import forms

app_name = 'study_platform'
urlpatterns = [
    path('', views.home_view, name='home'),                    # Will be changed to home page when made
    path('register/', views.register_view, name='register'),   # For the registration page
    path('login/', views.login_view, name='login'),            # For the login page
    path('profile/', views.profile_view, name='profile'),      # For the profile page
    path('shop/', views.shop, name='shop'),                    # For the shop page
]
