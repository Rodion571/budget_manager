from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, UserLoginForm

User = get_user_model()

def register(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
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

def user_login(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin:index')
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

def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    Handle user logout.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: The HTTP response redirect object.
    """
    logout(request)
    return redirect(reverse('home_content'))

def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home content page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    return render(request, 'home_content.html')

class CustomLoginView(auth_views.LoginView):
    """
    Custom login view using Django's built-in authentication view.

    Attributes:
        template_name (str): The template to use for rendering the login page.
    """
    template_name = 'accounts/login.html'

def set_language(request: HttpRequest) -> HttpResponseRedirect:
    """
    Set the user's preferred language.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: The HTTP response redirect object.
    """
    user_language = request.GET.get('language', 'en')
    activate(user_language)
    response = redirect(request.META.get('HTTP_REFERER'))
    response.set_cookie('django_language', user_language)
    return response
