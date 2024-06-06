from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.contrib import admin


class storage(models.Model):
    ID = models.AutoField(primary_key= True)
    Name = models.CharField(max_length=255 , unique= True , null= False , blank= False)
    amount = models.PositiveIntegerField(null= False , blank= False , validators= [
        validators.MinValueValidator(0,"error")
        ])



class Products(models.Model) :
    ID = models.AutoField(primary_key= True)
    Name = models.CharField(max_length=255 , unique= True , null= False , blank= False)
    Price = models.PositiveIntegerField( null= False , blank= False )
    suger = models.PositiveIntegerField()
    coffee = models.PositiveIntegerField()
    flour= models.PositiveIntegerField()
    chocolate = models.PositiveIntegerField()
    vertical = models.BinaryField(max_length=10) #ASk


class Orders(models.Model) :
    Order_ID = models.AutoField(primary_key=True , unique= True)
    Username = models.CharField(max_length=255)
    Products = models.CharField(max_length=255)
    Purchase_amount = models.IntegerField()
    Type = models.BooleanField(default= True) #ASK 


class Orders_Product(models.Model) :
    ID = models.AutoField(primary_key= True)
    prodect_id = models.ForeignKey(Products , on_delete= models.CASCADE)
    orders_orderid = models.ForeignKey(Orders , on_delete= models.CASCADE)
    
class Users_Orders(models.Model) :
    Users_username = models.ForeignKey(User , on_delete= models.CASCADE , null = True)
    Orders_orderID = models.ForeignKey(Orders , on_delete= models.CASCADE , null = True)

    class Meta:
        unique_together = ('Users_username', 'Orders_orderID')

