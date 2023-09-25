from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import re

def home(request):
    return render(request , 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request , 'This username is already taken. Please choose a different username.')
                return redirect("register")

            if User.objects.filter(email=email).exists():
                messages.error(request , 'This email is already registered. Please use a different email.')
                return redirect('register')
            
            if not password[0].isupper():
                messages.error(request , 'Password must start with a capital letter.')
                return redirect('register')
            
            if len(password) < 8:
                messages.error(request , 'Password must be at least 8 characters long.')
                return redirect('register')

            if not re.search(r'\d', password):
                messages.error(request , 'Password must contain at least one number.')
                return redirect('register')
            
            user = User(username=username,email=email)
            user.set_password(password)
            user.save()
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')

    else:
        form = UserRegisterForm()
    return render(request , 'register.html' , {'form':form})


def login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('emailorusername') 
        password = request.POST.get('password')

        if not email_or_username:
            messages.error(request, 'Username or email is required.')
            return redirect('login')

        if not password:
            messages.error(request, 'Password is required.')
            return redirect('login')

        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html', {'title': 'Login'})
