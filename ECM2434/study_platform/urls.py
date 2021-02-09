from django.urls import path
from . import views
from . import forms

app_name = 'study_platform'
urlpatterns = [
    path('', views.register_view, name='register'),           #Will be changed to home page when made
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login')
]
