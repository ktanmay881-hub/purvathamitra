from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.supplier_register, name='supplier_register'),
    path('login/', views.supplier_login, name='supplier_login'),
    # path('dashboard/', views.supplier_dashboard, name='supplier_dashboard'),

    path('', views.dashboard, name='supplier_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('inventory/', views.inventory, name='inventory'),
    path('orders/', views.orders, name='orders'),
    path('account/', views.account, name='account'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout_view, name='logout'),
    path('inventory/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('inventory/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('orders/deliver/<int:order_id>/', views.mark_delivered, name='mark_delivered'),

]

