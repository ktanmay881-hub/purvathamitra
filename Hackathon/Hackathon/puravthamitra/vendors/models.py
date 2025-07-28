from django.db import models
from django.contrib.auth.models import User
from suppliers.models import Product

ORDER_STATUS_CHOICES = [
    ('In Process', 'In Process'),
    ('Completed', 'Completed'),
]

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.shop_name or self.user.username

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.product.price_per_kg

class Order(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='In Process')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.vendor.username}"

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())
