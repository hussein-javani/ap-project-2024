from django.contrib import admin
from .models import *

admin.site.register(Storage, )
admin.site.register(Products, )
admin.site.register(Orders, )
admin.site.register(Orders_Product, )

