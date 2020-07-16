from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # status can be either 'Delivering', 'Completed' or 'Canceled'
    STATUSES = [
        (0, 'Delivering'),
        (1, 'Completed'),
        (2, 'Cancelled')
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
