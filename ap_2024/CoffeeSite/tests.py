from django.test import TestCase

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your tests here.

def test_home(request):
    return render(request, "home.html", context={"list":range(0,10)})

def test_login(request):
    return render(request, "login.html", )

def test_signup(request):
    return render(request, "signup.html", )
    
def test_history(request):
    return render(request, "orderhistory.html", context={"list":range(0,3)})
    










