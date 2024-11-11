from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm

from django.contrib.auth import get_user_model

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home_content'))
            else:
                print("Пользователь не аутентифицирован после регистрации.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home_content'))
            else:
                form.add_error(None, 'Неверные учетные данные')
                print("Ошибка аутентификации: неверные учетные данные.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('home_content'))

def home(request):
    return render(request, 'home.html')


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

