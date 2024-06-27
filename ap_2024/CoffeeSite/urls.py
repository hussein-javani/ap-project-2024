from django.urls import path
from . import views
from . import tests

# urlpatterns = [
#     path('test/home/', tests.test_home,),
#     path('test/', tests.test_home, name='home'),
#     path('test/login/', tests.test_login, name='login'),
#     path('test/signup/', tests.test_signup, name='signup'),
#     path('test/history/', tests.test_history, name='history'),
#     path('test/cart/', tests.test_cart, name='cart'),
#     path('test/admin/stats', tests.test_admin_stats, name='stats'),
#     path('test/admin/storage', tests.test_admin_storage, name='storage'),
#     path('test/admin/addproduct', tests.test_admin_addproduct, name='addproduct'),
#     path('test/admin/', tests.test_redirect_stats, name="redirect-stats"),
# ]

urlpatterns = [
    path('test/home/', tests.test_home,),
    path('test/', tests.test_home, name='home'),
    path('login/', views.login_view, name='login'), # ok
    path('signup/', views.signup_view, name='signup'), # ok
    path('test/history/', tests.test_history, name='history'),
    path('test/cart/', tests.test_cart, name='cart'),
    path('test/admin/stats', tests.test_admin_stats, name='stats'),
    path('test/admin/storage', tests.test_admin_storage, name='storage'),
    path('test/admin/addproduct', tests.test_admin_addproduct, name='addproduct'),
    path('test/admin/', tests.test_redirect_stats, name="redirect-stats"),
]
