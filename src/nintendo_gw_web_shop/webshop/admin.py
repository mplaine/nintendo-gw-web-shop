from webshop.models import Type, Product, SaleItem, Statistic, Address, Comment, Rating, ShippingMethod, Order, OrderItem
from django.contrib import admin
	

"""
Administration UI for types.

Author(s): Markku Laine
"""
class TypeAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "name" ] } ),
		( "Images",				{ "fields" : [ "image", "imageThumb" ], "classes" : [ "collapse" ] } ),
	]
	list_display	= ( Type.__unicode__, "image", "imageThumb" )
	ordering		= [ "name" ]
	search_fields	= [ "name" ]
admin.site.register( Type, TypeAdmin )


"""
Administration UI for products.

Author(s): Markku Laine
"""
class ProductAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "title", "type", "model", "dateOfRelease", "produced", "rarity", "description", "quantity" ] } ),
		( "Images",				{ "fields" : [ "image", "imageThumb" ], "classes" : [ "collapse" ] } ),
	]
	list_display	= ( "title", "type", "model", "dateOfRelease", "produced", "rarity", "quantity", "image", "imageThumb" )
	list_filter		= [ "type", "quantity", "rarity" ]
	ordering		= [ "title" ]
	search_fields	= [ "title", "model" ]
	date_hierarchy	= "dateOfRelease"
admin.site.register( Product, ProductAdmin )


"""
Administration UI for sale items.

Author(s): Markku Laine
"""
class SaleItemAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "product", "price", "onSale" ] } ),
	]
	list_display	= ( "product", "price", "onSale" )
	list_filter		= [ "onSale", "price" ]
	ordering		= [ "product__title" ]
admin.site.register( SaleItem, SaleItemAdmin )


"""
Administration UI for statistics.

Author(s): Markku Laine
"""
class StatisticAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "product", "numberOfViews" ] } ),
	]
	list_display	= ( "product", "numberOfViews" )
	list_filter		= [ "numberOfViews" ]
	ordering		= [ "product__title" ]
admin.site.register( Statistic, StatisticAdmin )


"""
Administration UI for addresses.

Author(s): Markku Laine
"""
class AddressAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "user", "streetAddressLine1", "streetAddressLine2", "zipCode", "city", "state", "country" ] } ),
	]
	list_display	= ( "user", "streetAddressLine1", "zipCode", "city", "country" )
	list_filter		= [ "city", "country" ]
	ordering		= [ "user__username" ]
	search_fields	= [ "streetAddressLine1" ]
admin.site.register( Address, AddressAdmin )


"""
Administration UI for comments.

Author(s): Markku Laine
"""
class CommentAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "user", "product", "contents", "commentsOn", "published" ] } ),
	]
	list_display	= ( "user", "product", "contents", "commentsOn", "published" )
	list_filter		= [ "user", "product" ]
	ordering		= [ "user__username" ]
	search_fields	= [ "contents" ]
	date_hierarchy	= "published"
admin.site.register( Comment, CommentAdmin )


"""
Administration UI for ratings.

Author(s): Markku Laine
"""
class RatingAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "user", "product", "rate" ] } ),
	]
	list_display	= ( "user", "product", "rate" )
	list_filter		= [ "rate", "user", "product" ]
	ordering		= [ "user__username" ]
admin.site.register( Rating, RatingAdmin )


"""
Administration UI for ratings.

Author(s): Markku Laine
"""
class ShippingMethodAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "name", "description", "price", "onSale" ] } ),
	]
	list_display	= ( "name", "price", "onSale" )
	list_filter		= [ "onSale", "price" ]
	ordering		= [ "name" ]
admin.site.register( ShippingMethod, ShippingMethodAdmin )


"""
Administration UI for orders.

Author(s): Markku Laine
"""
class OrderAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "user", "date", "shippingMethod", "paid", "delivered" ] } ),
	]
	list_display	= ( "user", "shippingMethod", "paid", "delivered", "date" )
	list_filter		= [ "user", "paid", "delivered", "date" ]
	ordering		= [ "user__username" ]
	date_hierarchy	= "date"
admin.site.register( Order, OrderAdmin )


"""
Administration UI for orders.

Author(s): Markku Laine
"""
class OrderItemAdmin( admin.ModelAdmin ):
	fieldsets		= [
		( "Basic Information",	{ "fields" : [ "order", "saleItem", "quantity" ] } ),
	]
	list_display	= ( "order", "saleItem", "quantity" )
	list_filter		= [ "order" ]
	ordering		= [ "order__id" ]
admin.site.register( OrderItem, OrderItemAdmin )