from django.urls import path
from . import views
from . import forms

app_name = 'study_platform'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.home_view, name='login')
]
