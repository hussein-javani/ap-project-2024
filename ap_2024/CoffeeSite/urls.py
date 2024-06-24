from django.urls import path
from . import views
from . import tests

urlpatterns = [
    path('test/home/', tests.test_home, name='home'),
]