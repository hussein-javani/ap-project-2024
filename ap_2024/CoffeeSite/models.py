from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.contrib import admin


class storage(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255 , unique= True , null= False , blank= False)
    amount = models.PositiveIntegerField(null= False , blank= False , validators= [
        validators.MinValueValidator(0,"error")
        ])



class Products(models.Model) :
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255 , unique= True , null= False , blank= False)
    #null and blank are set false so if tthe product doesn't have one items , its value must be 0 not null.
    price = models.PositiveIntegerField(null= False , blank= False )
    suger = models.PositiveIntegerField(null= False , blank= False)
    coffee = models.PositiveIntegerField(null = False , blank=False)  
    flour= models.PositiveIntegerField(null= False , blank= False)
    chocolate = models.PositiveIntegerField(null= False , blank= False)
    vertical = models.BinaryField(max_length=10) #ASk

    def check_storage(self) : 
        stored_suger = storage.objects.filter(name = "suger").first()
        stored_coffee = storage.objects.filter(name = "coffee").first()
        stored_flour = storage.objects.filter(name = "flour").first()
        stored_chocolate = storage.objects.filter(name = "chocolate").first()

        return (stored_suger.amount >= self.suger and stored_coffee.amount >= self.coffee and stored_chocolate.amount>= self.chocolate and stored_flour.amount >= self.flour)
            
        

    def calculate_price(self) :
        if self.check_storage() :
            return self.price
        


class Orders(models.Model) :
    order_id = models.AutoField(primary_key=True , unique= True)
    username = models.CharField(max_length=255)
    products = models.CharField(max_length=255)
    purchase_amount = models.IntegerField()
    type = models.BooleanField(default= True) #ASK 


class Orders_Product(models.Model) :
    id = models.AutoField(primary_key= True)
    prodect_id = models.ForeignKey(Products , on_delete= models.CASCADE)
    order_id = models.ForeignKey(Orders , on_delete= models.CASCADE)
    
class Users_Orders(models.Model) :
    username = models.ForeignKey(User , on_delete= models.CASCADE , null = True)
    orderID = models.ForeignKey(Orders , on_delete= models.CASCADE , null = True)

    class Meta:
        unique_together = ('username', 'orderID')

