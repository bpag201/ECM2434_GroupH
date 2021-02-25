from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .utils import paging, get_page
from .forms import User
from .models import UserProfile, Course

# Create your views here.

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
        print("a")
        form = UserCreationForm(data=request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("b")
            form.save()
            print("save")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(username)
            print(raw_password)
            user = authenticate(username=username, password=raw_password)
            print("authenticated")
            login(request, user)
            print("logged in")
            return redirect('/profile')
    else:
        print("c")
        form = UserCreationForm()
    print("d")
    return render(request, "register.html", {'form': form})


'''
    This view is used to authenticate and log in a user. If login is authenticated then it takes them directly to their
    profile page
'''


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            print("form valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("logged in")
                # messages.info(request, f"You are now logged in as {username}")
                print("blast off")
                return redirect('/profile')
            else:
                messages.error(request, "Invalid username or password")
        else:
            print("form invalid")
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "login.html", {'form': form})


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

    # user_login_name = request.session['user_login_name']

    # we have to decide another credential for login since real name can be duplicated
    # cur_user = get_object_or_404(User, full_name=user_login_name)

    cur_user = request.user

    """Error: the following code will raise an error, since when a user is registered, only the user object is created, 
       But not the user profile."""

    # try:
    #     cur_user_profile = cur_user.userprofile
    # except Exception:
    #     cur_user_course = Course(name='Bsc Computer Science')
    #     cur_user_course.save()
    #     cur_user_profile = UserProfile(user=cur_user, nickname=cur_user.username, course=cur_user_course, avatar='/static/images/bex3.jpg')
    #     cur_user_profile.save()
    # cur_user_fullname = cur_user.first_name + cur_user.last_name
    # pars = {
    #     'real_name': cur_user_fullname,
    #     'nick_name': cur_user_profile.nickname,
    #     'email': cur_user.email,
    #     'college': cur_user_profile.course.college,
    #     'DOB': cur_user_profile.date_of_birth,
    #     'resource': cur_user_profile.resource,
    #     'achievement': cur_user_profile.achievement_set.all(),
    #     'team': cur_user_profile.team,  # can a user join more than one team?
    #     'user_tier': cur_user_profile.user_tier  # maybe wrong value
    # }
    return render(request, "profile_me.html")


""" the following pages are solely web pages which has no communication with the database yet, but only skeletons
    which describes what the corresponding functions should look like. """


def shop(request):
    return render(request, 'shop.html')


def create_card(request):
    return render(request, 'create_new_card.html')


def answer_quiz(request):
    return render(request, 'answer_quiz.html')


def flash_card(request):
    return render(request, 'flash_card.html')


""" In order to implement pagination on the web page, several testing data is added to this function """


def card_set_list(request):
    sample1 = {
        "Title": "Sample1",
        "Description": "zhubao zhui diao",
        "Author": "HuangJie",
        "Tags": ["HuangJie1", "HuangJie2", "HuangJie3"]
    }
    sample2 = {
        "Title": "Sample1",
        "Description": "zhubao zhui diao",
        "Author": "ZhuBao",
        "Tags": ["ZhuBao1", "ZhuBao2", "ZhuBao3"]
    }
    pars = {
        "card_sets": [sample1, sample2, sample1, sample2, sample1, sample2, sample1, sample2]
    }
    pars2 = paging(pars["card_sets"])
    if request.GET.get("pg_num"):
        pg_num = int(request.GET.get("pg_num"))
    else:
        pg_num = 1
    pg_obj = get_page(pg_num, pars2)
    output = {
        "card_sets": pg_obj,
        "pg_size": len(pars2),
        "cur_page": pg_num
    }
    return render(request, 'card_sets.html', output)
