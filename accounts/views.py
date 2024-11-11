from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('home_content'))
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

from flask import Flask, request, redirect, url_for, render_template
from django.contrib.auth import authenticate, login
from your_app.forms import UserLoginForm  # Путь к вашей форме

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        form = UserLoginForm(data=request.form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(url_for('home_content'))  # Flask использует url_for для перенаправлений
    else:
        form = UserLoginForm()
    return render_template('login.html', {'form': form})

@app.route('/home')
def home_content():
    return 'Welcome to the home page!'

if __name__ == '__main__':
    app.run()

def user_logout(request):
    logout(request)
    return redirect(reverse('home_content'))

def home(request):
    return render(request, 'home.html')


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

