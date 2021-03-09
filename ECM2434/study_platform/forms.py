from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .texts import *


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150,
                               min_length=6,
                               label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text=usenm_helptxt,
                               error_messages={
                                   "required": usrnm_errmsg_require,
                                   "min_length": usrnm_errmsg_length,
                                   "max_length": usrnm_errmsg_length
                               })
    fstname = forms.CharField(max_length=150,
                              label="First Name",
                              widget=forms.TextInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  "required": name_errmsg_require,
                                  "max_length": name_errmsg_length
                              })
    sndname = forms.CharField(max_length=150,
                              label="Second Name",
                              widget=forms.TextInput(attrs={'class': 'form-control col'}),
                              error_messages={
                                  "required": name_errmsg_require,
                                  "max_length": name_errmsg_length
                              }
                              )
    paswd1 = forms.CharField(min_length=8,
                             label="Password",
                             widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}),
                             help_text=paswd_helptxtx,
                             error_messages={
                                 "required": paswd_errmsg_require,
                                 "min_length": paswd_errmsg_length
                             })
    paswd2 = forms.CharField(min_length=8,
                             label="Confirm",
                             widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}),
                             error_messages={
                                 "required": paswd_errmsg_require,
                                 "min_length": paswd_errmsg_length
                             })
    email = forms.EmailField(required=True,
                             label="E-mail",
                             validators=[EmailValidator],
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             error_messages={
                                 "required": email_errmsg_require,
                                 "invalid": email_errmsg_style
                             })

    def clean_username(self):
        usrname = self.cleaned_data.get('username')
        if User.objects.filter(username=usrname):
            raise ValidationError(usrnm_errmsg_exist)
        else:
            return usrname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise ValidationError(email_errmsg_exist)
        else:
            return email

    def clean_paswd1(self):
        pwd = self.cleaned_data.get('paswd1')
        if validate_password(pwd) is None:
            return pwd

    def clean_paswd2(self):
        pwd1 = self.cleaned_data.get('paswd1')
        pwd2 = self.cleaned_data.get('paswd2')
        if pwd1 != pwd2:
            raise ValidationError(paswd_errmsg_mismatch)
        else:
            return pwd2


