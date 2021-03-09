from django.urls import path
from . import views
from . import forms

app_name = 'study_platform'
urlpatterns = [
    path('', views.home_view, name='home'),                             # Will be changed to home page when made
    path('register/', views.register_view, name='register'),            # For the registration page
    path('login/', views.login_view, name='login'),                     # For the login page
    path('profile/', views.profile_view, name='profile'),               # For the profile page
    path('shop/', views.shop, name='shop'),                             # For the shop page
    path('answer_quiz/', views.answer_quiz, name='answer_quiz'),        # For the quiz-answering page
    path('card_set_list/', views.card_set_list, name='card_set_list'),  # For viewing all possible card sets
    path('flash_card/', views.flash_card, name='flash_card'),           # For viewing a flash card set, which could also
                                                                        # be used for quiz cards
    path('get_resource/', views.get_resource, name='get_resource'),     # For getting the resources from the database
    path('set_resource/', views.set_resource, name='set_resource'),     # For setting the user's resources to the given resource
    path('edit_set/', views.edit_set, name='edit_set'),
    path('view_set/', views.view_set, name='view_set'),
    path('navigation/', views.navigation_view, name='navigation'),
    path('result/', views.result, name='result'),
]
