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
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('test/history/', tests.test_history, name='history'), #TODO
    path('cart/', views.cart_view, name='cart'),
    path('test/admin/stats', tests.test_admin_stats, name='stats'), #TODO
    path('admin/storage', views.storage_view, name='storage'),
    path('admin/addproduct', views.add_product_view, name='addproduct'),
    path('test/admin/', tests.test_redirect_stats, name="redirect-stats"),
    
    path('add-to-cart', views.add_to_cart_view , name="add-to-cart"),
    path('remove-product', views.remove_product_view , name="remove-product"),
    path('update-product', views.update_product_view , name="update-product"),
    path('takeout', views.take_out_view , name="takeout"),
]
