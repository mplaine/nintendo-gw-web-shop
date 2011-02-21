from django.db import models
from django.contrib.auth.models import User


# Categories: Silver, Gold, etc.
class Type( models.Model ):
	name 					= models.CharField( max_length=50, unique=True )
	IMAGE_UPLOAD_TO			= "images/types"
	image					= models.ImageField( upload_to=IMAGE_UPLOAD_TO, max_length=255 )
	imageThumb				= models.ImageField( "Image thumb", upload_to=IMAGE_UPLOAD_TO + "/thumbs", max_length=255 )
	
	def __unicode__( self ):
		return self.name + " Series"


# Games: Ball, Flagman, etc.
class Product( models.Model ):
	title					= models.CharField( max_length=50 )
	type					= models.ForeignKey( Type )
	model					= models.CharField( max_length=20 )
	dateOfRelease			= models.DateField( "Date of release" )
	produced				= models.IntegerField( default=0 )
	RARITY_VERY_COMMON		= 1
	RARITY_COMMON			= 2
	RARITY_RARE				= 3
	RARITY_VERY_RARE		= 4
	RARITY_EXTREMELY_RARE	= 5
	RARITY_CHOICES	= (
		( RARITY_VERY_COMMON, "Very common" ),
		( RARITY_COMMON, "Common" ),
		( RARITY_RARE, "Rare" ),
		( RARITY_VERY_RARE, "Very rare" ),
		( RARITY_EXTREMELY_RARE, "Extremely rare" ),
	)
	rarity					= models.IntegerField( choices=RARITY_CHOICES )
	description				= models.TextField()
	quantity				= models.IntegerField( default=0 )
	IMAGE_UPLOAD_TO			= "images/products"
	image					= models.ImageField( upload_to=IMAGE_UPLOAD_TO, max_length=255 )
	imageThumb				= models.ImageField( "Image thumb", upload_to=IMAGE_UPLOAD_TO + "/thumbs", max_length=255 )

	def __unicode__( self ):
		return self.title + " (" + self.type.__str__() + ")"
	
	def get_averageRating(self):
		average = 0
		if self.rating_set.count > 0:
			for rating in self.rating_set:
				average +=rating.rate
			return (average / self.rating_set.count)
		else:
			return 0


# Sales: games with price information
class SaleItem( models.Model ):
	price					= models.DecimalField( max_digits=7, decimal_places=2 )
	product					= models.ForeignKey( Product )
	onSale					= models.BooleanField( "On sale", default=True)

	def __unicode__( self ):
		return self.product.__str__() + u", %.2f \u20AC" % ( self.price, )


# Statistics: # of views only, because # of comment, # of sales, and average rating can be calculated?
class Statistic( models.Model ):
	product					= models.ForeignKey( Product )
	numberOfViews			= models.IntegerField( default=0 )
	
	def __unicode__( self ):
		return self.product.__str__() + ": %d views" % ( self.numberOfViews, )
		

# Addresses of the user
class Address( models.Model ):
	user				= models.ForeignKey( User )
	streetAddressLine1 	= models.CharField( "Street address line 1", max_length=100 )
	streetAddressLine2 	= models.CharField( "Street address line 2", max_length=100, blank=True )
	zipCode				= models.CharField( max_length=10 )
	city 				= models.CharField( max_length=50 )
	state				= models.CharField( max_length=50, blank=True )
	country				= models.CharField( max_length=50, default="Finland" )

		
class Comment( models.Model ):
	user 		= models.ForeignKey( User )
	published 	= models.DateTimeField( "Date published" )
	contents 	= models.TextField()
	commentsOn 	= models.ForeignKey( "self" )
	product		= models.ForeignKey( Product )


class Rating( models.Model ):
	rate		= models.IntegerField() #TODO MAX & MIN values
	user 		= models.ForeignKey( User )
	product		= models.ForeignKey( Product )


class Order( models.Model ):
	date		= models.DateTimeField()
	user 		= models.ForeignKey( User )
	delivered	= models.BooleanField()
	paid		= models.BooleanField()
	# List of SaleItems needs to be added

class OrderItem( models.Model ):
	saleItem				= models.ForeignKey( SaleItem )
	order					= models.ForeignKey( Order )
	quantity				= models.IntegerField( default=1 )

	def __unicode__( self ):
		return self.id

# Deprecated: replaced by Order class 
#class ShoppingCart(models.Model):

# Users: Teemu Teekkari, Arto Assari, etc.
#class User( models.Model ):
#	firstName 			= models.CharField( "First name", max_length=50 )
#	lastName 			= models.CharField( "Last name", max_length=50 )
#	password			= models.CharField( max_length=128 )
#	email 				= models.EmailField()


#class Product(models.Model):
#	numOfComments 	= models.IntegerField() 
#	numOfViews 		= models.IntegerField() 
#	numOfPurchases 	= models.IntegerField()

#class ProductDetails(models.Model):
#	product			= models.ForeignKey( Product )
#	name 			= models.CharField(max_length=50)
#	description		= models.CharField(max_length=1023)
#	picture 		= models.URLField() 
#	price 			= models.DecimalField(decimal_places=2, max_digits=6) 
#	quantity 		= models.IntegerField()


#class ProductOrder(models.Model):
#	details 	= models.ForeignKey(ProductDetails)
#	quota		= models.IntegerField()
#	order		= models.ForeignKey(Order)

#class Review(models.Model):
#	user 		= models.ForeignKey(User)
#	published 	= models.DateTimeField('date published')
#	contents	= models.TextField()