from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma

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

	def average(self):
		result = 0
		index = 0
		for temp in self.rating_set.all():
			result += temp.rate
			index += 1
		if result > 0:
			return ( result / index )
		else:
			return result
		
	def dummylist(self):
		my_list = [1, 2, 3, 4, 5]
		return my_list
	
	def filteredcomments(self):
		result_list = []
		firstlayer = self.comment_set.filter(commentsOn=None)
		for x in firstlayer:
			result_list.append(x)
			temp_list_1 = self.comment_set.filter(commentsOn=x)
			for y in temp_list_1:
				result_list.append(y)
				temp_list_2 = self.comment_set.filter(commentsOn=y)
				for z in temp_list_2:
					result_list.append(z)
		return result_list
	
	def ownrating(self, user):
		rating	= 0
		try:
			rate = self.rating_set.get(user=user)
			rating	= rate.rate
		except Rating.DoesNotExist:
			rating = 0
		return rating

# Sales: games with price information
class SaleItem( models.Model ):
	price					= models.DecimalField( max_digits=7, decimal_places=2 )
	product					= models.ForeignKey( Product )
	onSale					= models.BooleanField( "On sale", default=True )

	def getPriceInEuros( self ):
		return u"%.2f \u20AC" % ( self.price, )

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
	zipCode				= models.CharField( "ZIP code", max_length=10 )
	city 				= models.CharField( max_length=50 )
	state				= models.CharField( max_length=50, blank=True )
	country				= models.CharField( max_length=50, default="Finland" )

	def __unicode__( self ):
		return self.user.first_name + " " + self.user.last_name + " (" + self.user.username + "), " + self.streetAddressLine1 + ( ", " + self.streetAddressLine2 if self.streetAddressLine2 is None else "" ) + ", " + self.zipCode + " " + self.city + ( ", " + self.state if self.state is None else "" ) + ", " + self.country
		
class Comment( models.Model ):
	user 		= models.ForeignKey( User )
	published 	= models.DateTimeField( "Date published" )
	contents 	= models.TextField()
	commentsOn 	= models.ForeignKey( "self", null=True, blank=True )
	product		= models.ForeignKey( Product )


class Rating( models.Model ):
	rate		= models.IntegerField()
	user 		= models.ForeignKey( User )
	product		= models.ForeignKey( Product )

class ShippingMethod( models.Model ):
	name		= models.CharField( max_length=50 )
	description	= models.TextField( blank=True )
	price		= models.DecimalField( max_digits=5, decimal_places=2 )
	onSale		= models.BooleanField( "On sale", default=True )

	def getPriceInEuros( self ):
		return u"%.2f \u20AC" % ( self.price, )

	def __unicode__( self ):
		return self.name + u", %.2f \u20AC" % ( self.price, )

class Order( models.Model ):
	date			= models.DateTimeField()
	user 			= models.ForeignKey( User )
	delivered		= models.BooleanField()
	paid			= models.BooleanField()
	shippingMethod	= models.ForeignKey( ShippingMethod )

	def getPriceInEuros( self ):
		return u"%.2f \u20AC" % ( self.price, )

	def getOrderItems( self ):
		return OrderItem.objects.filter( order=self )

	def getSubtotal( self ):
		subtotal		= 0
		orderItems		= OrderItem.objects.filter( order=self )

		for orderItem in orderItems:
			subtotal	= subtotal + ( orderItem.quantity * orderItem.saleItem.price )
		return subtotal

	def getSubtotalInEuros( self ):
		return u"%.2f \u20AC" % ( self.getSubtotal(), )

	def getTotal( self ):
		return self.getSubtotal() + self.shippingMethod.price

	def getTotalInEuros( self ):
		return u"%.2f \u20AC" % ( self.getTotal(), )

	def __unicode__( self ):
		return "%s (%s %s)" % ( self.date, self.user.first_name, self.user.last_name )
		
class OrderItem( models.Model ):
	saleItem				= models.ForeignKey( SaleItem )
	order					= models.ForeignKey( Order )
	quantity				= models.IntegerField( default=1 )

	def getPrice( self ):
		return self.quantity * self.saleItem.price

	def getPriceInEuros( self ):
		return u"%.2f \u20AC" % ( self.getPrice(), )
	
	def __unicode__( self ):
		return "%d" % self.id