from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
# from models import UserProfile

# '''
#     Sets the given user's resources (currency) to the given value
# '''
# def set_resource(resource, username):
#     UserProfile.objects
#     User.objects

#     user = UserProfile(user=User(username=username))

#     user.resource = resource

# '''
#     Gets the given user's resources
# '''
# def get_resource(username):
#     UserProfile.objects
#     User.objects

#     user = UserProfile(user=User(username=username))

#     resource = user.resource
#     return resource

# Create your views here.
'''
    This is the view used to authenticate and create a new user when they register. If the registration is authenticated
    then the user is logged in and taken to their profile page.
'''
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form':form})

'''
    This view is used to authenticate and log in a user. If login is authenticated then it takes them directly to their
    profile page
'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}")
                return redirect('/profile')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "login.html", {'form':form})

'''
    Simply takes the user to the homepage.
'''
def home_view(request):
    return render(request, "homepage.html")


def profile_view(request):
    """
    input: this page is designed to be redirected by a dash-board page, which stores the current user's login credential
    in session as 'user_login_name' (at the time I'm writing this code I assume we use the full_name in User model as
    the login name but it is obviously not appropriate)

    output: see pars
    """

    # This code is commented as it currently doesn't work
    
    # user_login_name = request.session['user_login_name']
    # we have to decide another credential for login since real name can be duplicated
    # cur_user = get_object_or_404(User, usename=user_login_name)
    # cur_user_profile = get_object_or_404(UserProfile, user=cur_user)
    # pars = {
    #     'real_name': cur_user.full_name,
    #     'nick_name': cur_user_profile.nickname,
    #     'email': cur_user.email,
    #     'college': cur_user_profile.course.college,
    #     'dob': cur_user.date_of_birth,
    #     'resource': cur_user_profile.resource,
    #     'achievement': cur_user.achievement_set.all(),
    #     'team': cur_user.team,  # can a user join more than one team?
    #     'user_tier': cur_user.user_tier.label  # maybe wrong value
    # }
    return render(request, "profile_me.html")#, pars)


def shop(request):
    return render(request, 'shop.html')
