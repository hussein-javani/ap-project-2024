from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views import View
from .forms import SignupForm, LoginForm
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # return HttpResponse("User not valid", status=401)
                return render( request, "login.html", { "form":form, "error" : "نام کاربری یا رمز عبور اشتباه است"})
                
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, "error":""})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.full_name = full_name
            user.save()

            # Log the user in
            login(request, user)

            # Redirect to a success page
            return redirect('home')  # Redirect to your home page or any other page
        else:
            return render(request, "signup.html", {"form":form, "error":"اطلاعات وارد شده معتبر نمی‌باشد"})
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


