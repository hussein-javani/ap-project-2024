from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError

class storage(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255 , unique= True , null= False , blank= False)
    amount = models.PositiveIntegerField(null= False , blank= False , validators= [
        validators.MinValueValidator(0,"error")
        ])



class Products(models.Model) :
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255 , unique= True , null= False , blank= False)

    price = models.PositiveIntegerField(null= False , blank= False)
    suger = models.PositiveIntegerField(null= False , blank= False)
    coffee = models.PositiveIntegerField(null = False , blank=False)  
    flour= models.PositiveIntegerField(null= False , blank= False)
    chocolate = models.PositiveIntegerField(null= False , blank= False)
    vertical = models.BinaryField(max_length=10) #ASk

    def check_storage(self , quantity) : 
        stored_suger = storage.objects.filter(name = "suger").first()
        stored_coffee = storage.objects.filter(name = "coffee").first()
        stored_flour = storage.objects.filter(name = "flour").first()
        stored_chocolate = storage.objects.filter(name = "chocolate").first()

    
        return (stored_suger.amount >= self.suger * quantity  and 
                stored_coffee.amount >= self.coffee * quantity and 
                stored_chocolate.amount>= self.chocolate * quantity and
                stored_flour.amount >= self.flour * quantity
                )
    
    def update_storage(self , quantity) :
        if self.check_storage(quantity) :
            stored_suger = storage.objects.filter(name = "suger").first().amount 
            stored_coffee = storage.objects.filter(name = "coffee").first().amount
            stored_flour = storage.objects.filter(name = "flour").first().amount
            stored_chocolate = storage.objects.filter(name = "chocolate").first().amount

            #reducing 
            stored_suger -= self.suger * quantity
            stored_flour -= self.flour * quantity
            stored_coffee -= self.coffee * quantity
            stored_chocolate -= self.chocolate * quantity
            #saving

            stored_suger.save()
            stored_flour.save()
            stored_coffee.save()
            stored_chocolate.save()

        
        


class Orders(models.Model) :  #سبد خرید
    order_id = models.AutoField(primary_key=True , unique= True)
    username = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    purchase_amount = models.IntegerField()
    type = models.BooleanField(default= True) # is 1 if the order is take out and 0 if

    
    def confirm_order(self) :
        pass

class Orders_Product(models.Model) : 
    id = models.AutoField(primary_key= True)
    product_id = models.ForeignKey(Products , on_delete= models.CASCADE)
    order_id = models.ForeignKey(Orders , on_delete= models.CASCADE)


    
class Users_Orders(models.Model) :
    username = models.ForeignKey(User , on_delete= models.CASCADE , null = True)
    orderID = models.ForeignKey(Orders , on_delete= models.CASCADE , null = True)

    class Meta:
        unique_together = ('username', 'orderID')

    def calculate_overall_price(self):
        total_price = 0
        user_orders = Users_Orders.objects.filter(username=self.username)
        for user_order in user_orders:
            total_price += user_order.order.calculate_overall_price()
        return total_price
