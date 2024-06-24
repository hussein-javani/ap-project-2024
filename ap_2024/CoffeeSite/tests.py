from django.test import TestCase

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your tests here.

def test_home(request):
    return render(request, "home.html")
    
    
