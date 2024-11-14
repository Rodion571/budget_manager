from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email',]

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
