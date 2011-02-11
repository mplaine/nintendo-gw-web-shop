from django.db import models
from django.contrib.localflavor.fi.forms import FIZipCodeField


# Create your models here.
class User(models.Model):
	firstName 		= models.CharField( max_length=30 )
	lastName 		= models.CharField( max_length=30 )
	email 			= models.EmailField()
	streetAddress 	= models.CharField( max_length=50 )
	city 			= models.CharField( max_length=20 )
	zipCode			= FIZipCodeField
	password		= models.CharField( max_length=30 )
	country			= models.CharField( max_length=30 )
	
class Product(models.Model):
	numOfComments 		= models.IntegerField() 
	numOfViews 		= models.IntegerField() 
	numOfPurchases 		= models.IntegerField()

class ProductDetails(models.Model):
	product			= models.ForeignKey( Product )
	name 			= models.CharField(max_length=50)
	picture 		= models.URLField() 
	price 			= models.DecimalField(decimal_places=2, max_digits=6) 
	quantity 		= models.IntegerField()

class Comment(models.Model): 
	user 		= models.ForeignKey(User)
	published 	= models.DateTimeField('date published')
	contents 	= models.TextField()
	commentsOn 	= models.ForeignKey("self")

class Rating(models.Model):
	rate		= models.IntegerField() #TODO MAX & MIN values
	user 		= models.ForeignKey(User)

class Order(models.Model):
	date		= models.DateTimeField()
	user 		= models.ForeignKey(User)
	delivered	= models.BooleanField()
	paid		= models.BooleanField()
	

# Deprecated: replaced by Order class 
#class ShoppingCart(models.Model):


class ProductOrder(models.Model):
	details 	= models.ForeignKey(ProductDetails)
	quota		= models.IntegerField()
	order		= models.ForeignKey(Order)

class Review(models.Model):
	user 		= models.ForeignKey(User)
    	published 	= models.DateTimeField('date published')
	contents	= models.TextField()

