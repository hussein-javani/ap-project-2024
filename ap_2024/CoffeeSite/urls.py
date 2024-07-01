from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
    path('cart/', views.cart_view, name='cart'),
    path('admin/stats', views.stats_view, name='stats'),
    path('admin/', views.redirect_stats, name="redirect-stats"),
    path('admin/storage', views.storage_view, name='storage'),
    path('admin/addproduct', views.add_product_view, name='addproduct'),
    
    path('add-to-cart', views.add_to_cart_view , name="add-to-cart"),
    path('remove-product', views.remove_product_view , name="remove-product"),
    path('update-product', views.update_product_view , name="update-product"),
    path('takeout', views.take_out_view , name="takeout"),
    path('finalize-order', views.finalize_order_view , name="finalize-order"),
    path('delete-order', views.delete_order_view , name="delete-order"),
]
