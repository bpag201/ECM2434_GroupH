from django.urls import path
from . import views
from . import forms

app_name = 'study_platform'
urlpatterns = [
    path('templates/register', forms.register, name='register')
]
