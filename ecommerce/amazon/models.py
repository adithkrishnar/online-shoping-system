from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    PAYMENT = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS,
        default='pending'
    )

    payment = models.CharField(
        max_length=20,
        choices=PAYMENT,
        default='pending'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    address = models.TextField(default='Not Provided')

    phone = models.CharField(max_length=20, default="unknown")


    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name
