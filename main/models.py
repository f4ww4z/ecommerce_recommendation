from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField(default=0.0)


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField(default=0.0)
    # status can be either 'Delivering', 'Completed' or 'Canceled'
    STATUSES = [
        (0, 'Delivering'),
        (1, 'Completed'),
        (2, 'Cancelled')
    ]
    status = models.CharField(max_length=1, choices=STATUSES, default=0, help_text=mark_safe(
        "<ul><li>0 - Delivering</li><li>1 - Completed</li><li>2 - Cancelled</li></ul>"))


class ShoppingCart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
