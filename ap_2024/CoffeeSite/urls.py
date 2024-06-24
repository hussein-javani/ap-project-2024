from django.urls import path
from . import views
from . import tests

urlpatterns = [
    path('test/home/', tests.test_home, name='home'),
    path('test/login/', tests.test_login, name='login'),
]