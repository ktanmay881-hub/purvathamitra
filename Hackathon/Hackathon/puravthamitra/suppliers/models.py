from django.db import models
from django.contrib.auth.models import User

class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"
    



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Grains', 'Grains'),
        ('Vegetables', 'Vegetables'),
    ]

    supplier = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_name} ({self.supplier.username})"

    


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    customer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    expected_delivery = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('delivered', 'Delivered')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


