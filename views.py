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
    return render(request, "profile_me.html")


def shop(request):
    return render(request, 'shop.html')
