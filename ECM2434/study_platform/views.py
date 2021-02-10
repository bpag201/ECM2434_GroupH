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
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        print("c")
        form = UserCreationForm()
    print("d")
    return render(request, "register.html", {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                redirect('')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "login.html", {'form':form})

<<<<<<< Updated upstream
def home_view(request):
    return render(request, "homepage.html")
=======
User = get_user_model()
>>>>>>> Stashed changes
