from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

