# vendors/admin.py
from django.contrib import admin
from .models import Vendor, CartItem, Order

admin.site.register(Vendor)
admin.site.register(CartItem)
admin.site.register(Order)
