from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField( max_length=50)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()  
    sizes = models.ManyToManyField(Size, blank=True)

    def __str__(self):
        return self.name

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"Order for {self.quantity} {self.product.name}(s)"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username




    


    
