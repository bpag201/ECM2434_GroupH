from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model


# Create your views here.
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
    return render(request, "register.html", {'form':form})


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
                #messages.info(request, f"You are now logged in as {username}")
                print("blast off")
                return redirect('/profile')
            else:
                messages.error(request, "Invalid username or password")
        else:
            print("form invalid")
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "login.html", {'form':form})


def home_view(request):
    return render(request, "homepage.html")


def profile_view(request):
    """
    input: this page is designed to be redirected by a dash-board page, which stores the current user's login credential
    in session as 'user_login_name' (at the time I'm writing this code I assume we use the full_name in User model as
    the login name but it is obviously not appropriate)

    output: see pars
    """

    user_login_name = request.session['user_login_name']
    # we have to decide another credential for login since real name can be duplicated
    cur_user = get_object_or_404(User, full_name=user_login_name)
    pars = {
        'real_name': cur_user.full_name,
        'nick_name': cur_user.nickname,
        'email': cur_user.email,
        'college': cur_user.course.college,
        'dob': cur_user.date_of_birth,
        'resource': cur_user.resource,
        'achievement': cur_user.achievement_set.all(),
        'team': cur_user.team,  # can a user join more than one team?
        'user_tier': cur_user.user_tier.label  # maybe wrong value
    }
    return render(request, "profile_me.html", pars)


def shop(request):
    return render(request, 'shop.html')
