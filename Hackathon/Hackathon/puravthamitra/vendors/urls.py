from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='vendor_home'),
    path('login/', views.vendor_login, name='vendor_login'),
    path('register/', views.vendor_register, name='vendor_register'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('browse/', views.browse_products, name='browse_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # optional duplicate
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/delete/<int:order_id>/', views.delete_vendor_order, name='delete_vendor_order'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
   
]