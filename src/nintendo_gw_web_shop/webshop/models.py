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
	
class ProductDetails(models.Model):   
	name 			= models.CharField(max_length=50)
	picture 		= models.URLField() 
	price 			= models.DecimalField(decimal_places=2, max_digits=6) 
	quantity 		= models.IntegerField()
	
class Product(models.Model):
	details 		= models.ForeignKey( ProductDetails ) 
	numOfComments 	= models.IntegerField() 
	numOfViews 		= models.IntegerField() 
	numOfPurchases 	= models.IntegerField()