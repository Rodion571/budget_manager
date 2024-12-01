from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from .forms import UserRegisterForm, UserLoginForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Делаем пользователя активным
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home_content'))
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin:index')  # Перенаправление на админку для суперпользователей
            elif user is not None:
                login(request, user)
                return redirect('home_content')
            else:
                form.add_error(None, 'Неверные учетные данные')
        else:
            form.add_error(None, 'Некорректные данные формы')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect(reverse('home_content'))

def home(request):
    return render(request, 'home/home_content.html')

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

def set_language(request):
    user_language = request.GET.get('language', 'en')
    activate(user_language)
    response = redirect(request.META.get('HTTP_REFERER'))
    response.set_cookie('django_language', user_language)
    return response
