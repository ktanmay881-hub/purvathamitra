from django import forms
from django.contrib.auth.models import User
from .models import SupplierProfile

class SupplierRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = SupplierProfile
        fields = ['company_name', 'contact_number']

# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'quantity', 'price_per_kg', 'location', 'image']



