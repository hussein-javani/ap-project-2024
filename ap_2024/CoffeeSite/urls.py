from django.urls import path
from . import views
from . import tests

urlpatterns = [
    path('test/home/', tests.test_home, name='home'),
    path('test/login/', tests.test_login, name='login'),
    path('test/signup/', tests.test_signup, name='signup'),
    path('test/history/', tests.test_history, name='history'),
    path('test/cart/', tests.test_cart, name='history'),
]