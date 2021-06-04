from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''Relationships
     1-M
Customer- Orders
Product- Orders

    M-M
 Product-Tag
'''


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    profile_pic = models.ImageField(default="sagar_pic.jpg",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out door', 'Out door')
    )
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)


    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product.name

