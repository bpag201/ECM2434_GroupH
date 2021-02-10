from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


def register(request):
    submitted = False
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/register?submitted=True')
    else:
        form = RegisterForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'template/profile.html',
                  {'form': form, 'submitted': submitted}
                  )


User = get_user_model()
