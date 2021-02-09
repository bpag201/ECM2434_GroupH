from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def home_view(request):
    if request.method == 'POST':
        print("a")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("b")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        print("c")
        form = UserCreationForm()
    print("d")
    return render(request, "register.html")