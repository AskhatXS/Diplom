from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, PasswordInput

class CustomAuthForm(AuthenticationForm):
    # username = forms.CharField(widget=TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    # password = forms.CharField(widget=PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']
