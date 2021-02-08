from django.urls import path
from . import views

app_name = 'study_platform'
urlpatterns = [
    path('profile/self/', views.user_profile_self, name="profile_self"),
]

