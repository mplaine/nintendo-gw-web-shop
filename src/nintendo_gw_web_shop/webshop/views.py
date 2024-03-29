from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from webshop.forms import MyUserCreationForm, MyAuthenticationForm, MyUserChangeForm, MyPasswordResetForm, MyPasswordChangeForm, AddressForm
from webshop.models import Product, Type, Address, Order, Rating, Comment, Statistic, SaleItem, OrderItem, ShippingMethod
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
import md5

secret_key = '37e383c1182a6bab1524c9a7c0fc4557'

"""
Nintendo Game & Watch Shop

Root of the project.

Author(s): Markku Laine
"""
def root( request ):
	# Handle GET requests
	if request.method == "GET":
		return redirect( "webshop.views.home" )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Home

Author(s): Kalle Saila
"""
def home( request ):
	# Handle GET requests
	if request.method == "GET":
		# Retrieve all types
		types					= Type.objects.all().order_by( "name" )
		variables				= { "types" : types }
		context					= RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/index.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Home > Search Results

Author(s): Kalle Saila
"""
def search( request ):
	# Handle GET requests
	if request.method == "GET":
		querystring					= request.GET["q"]
		products					= Product.objects.filter(title__icontains=querystring).order_by( "title" )
		variables					= { "products" : products }
		context						= RequestContext( request )
		return render_to_response( "webshop/search.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Home > Category

Author(s): Kalle Saila
"""
def category( request, type_id ):
	# Handle GET requests
	if request.method == "GET":
		# Retrieve type
		type					= get_object_or_404( Type, id=type_id )
		variables				= { "type" : type }
		context					= RequestContext( request )
		return render_to_response( "webshop/category.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Register

Author(s): Markku Laine
"""
def register( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	# Create a new address. At first, associate a dummy user with the address
	address						= Address()
	dummyUser					= User()
	address.user				= dummyUser
	
	# Handle POST requests		
	if request.method == "POST":
		myUserCreationForm		= MyUserCreationForm( data=request.POST )
		addressForm				= AddressForm( data=request.POST, instance=address )

		# Check the validity of the forms
		if myUserCreationForm.is_valid() and addressForm.is_valid():
			user				= myUserCreationForm.save()
			# Automatically login the user after successful registration
			user.backend		= "django.contrib.auth.backends.ModelBackend"
			auth_login( request, user )
			# Retrieve the address
			userAddress			= addressForm.instance
			# Replace the dummy user with the currently logged-in user
			userAddress.user	= user
			# Save user's address
			userAddress.save()
			# After a successful registration, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			return redirect( next )
		else:
			#print "Forms are not valid!"
			# After a failed registration, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
	# Handle GET requests
	elif request.method == "GET":
		myUserCreationForm		= MyUserCreationForm( initial={} )
		addressForm				= AddressForm( initial={} )
		# After registration, redirect the user to the page (s)he came from based on 1) next URL parameter, 2) HTTP REFERER, and 3) default to home
		next					= request.GET.get( "next", request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) ) )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { "form" : myUserCreationForm, "next" : next, "addressForm" : addressForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/register.html", variables, context )


"""
Nintendo Game & Watch Shop > Login

Author(s): Markku Laine
"""
def login( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )
		
	# Handle POST requests		
	if request.method == "POST":
		myAuthenticationForm	= MyAuthenticationForm( data=request.POST )

		# Check the validity of the form
		if myAuthenticationForm.is_valid():
			## Retrieve username and password parameters
			username			= myAuthenticationForm.cleaned_data.get( "username", "" )
			password			= myAuthenticationForm.cleaned_data.get( "password", "" )
			# Authenticate and login the user
			user				= authenticate( username=username, password=password )
			auth_login( request, user )
			# After a successful login, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			return redirect( next )
		else:
			#print "Form is not valid!"
			# After a failed login, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
	# Handle GET requests
	elif request.method == "GET":
		myAuthenticationForm	= MyAuthenticationForm( initial={} )		
		# After login, redirect the user to the page (s)he came from based on 1) next URL parameter, 2) HTTP REFERER, and 3) default to home
		next					= request.GET.get( "next", request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) ) )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	# If the user comes from the password reset page, then redirect to the home page
	if next.find( "/webshop/passwordreset/" ) != -1:
		next					= reverse( "webshop.views.home" )

	variables					= { "form" : myAuthenticationForm, "next" : next }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/login.html", variables, context )	


"""
Nintendo Game & Watch Shop > Password Reset

Author(s): Markku Laine
"""
def password_reset( request ):
	# Handle GET requests
	if request.method == "GET":
		return redirect( "webshop.views.request_new_password" )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Password Reset > Request New Password

Author(s): Markku Laine
"""
def request_new_password( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	# Handle POST requests
	if request.method == "POST":
		myPasswordResetForm		= MyPasswordResetForm( data=request.POST )

		# Check the validity of the form
		if myPasswordResetForm.is_valid():
			# Email instructions to the user how to reset the password
			myPasswordResetForm.save( domain_override=None, use_https=False, token_generator=default_token_generator )
			return redirect( "webshop.views.new_password_requested" )
		#else:
			#print "Form is not valid!"
	# Handle GET requests
	elif request.method == "GET":
		myPasswordResetForm		= MyPasswordResetForm( initial={} )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { "form" : myPasswordResetForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/passwordreset/request_new_password.html", variables, context )	


"""
Nintendo Game & Watch Shop > Password Reset > New Password Requested

Author(s): Markku Laine
"""
def new_password_requested( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )
		
	# Handle GET requests
	if request.method == "GET":
		variables					= {}
		context						= RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/passwordreset/new_password_requested.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Password Reset > New Password Set

Author(s): Markku Laine
"""
def new_password_set( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )
		
	# Handle GET requests
	if request.method == "GET":
		variables					= {}
		context						= RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/passwordreset/new_password_set.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Logout

Author(s): Markku Laine
"""
def logout( request ):
	# Handle GET requests
	if request.method == "GET":
		# Logout the currently logged-in user
		auth_logout( request )
		# After a successful logout, redirect the user to the page (s)he came from based on 1) HTTP REFERER and 2) default to home
		next					= request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) )
		return redirect( next )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > My Account

Author(s): Markku Laine
"""
@login_required
def myaccount( request ):
	# Handle GET requests
	if request.method == "GET":
		return redirect( "webshop.views.account_details" )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > My Account > Account Details

Author(s): Markku Laine
"""
@login_required
def account_details( request ):
	# Handle POST requests
	if request.method == "POST":
		myUserChangeForm		= MyUserChangeForm( data=request.POST, instance=request.user )

		# Check the validity of the form
		if myUserChangeForm.is_valid():
			# Save changed account details
			myUserChangeForm.save()
			messages.success( request, "Account details have been successfully updated." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.account_details" )
		#else:
			#print "Form is not valid!"
	# Handle GET requests
	elif request.method == "GET":
		myUserChangeForm		= MyUserChangeForm( instance=request.user )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { "form" : myUserChangeForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/account_details.html", variables, context )


"""
Nintendo Game & Watch Shop > My Account > Change Password

Author(s): Markku Laine
"""
@login_required
def change_password( request ):
	# Handle POST requests
	if request.method == "POST":
		myPasswordChangeForm	= MyPasswordChangeForm( data=request.POST, user=request.user )

		# Check the validity of the form
		if myPasswordChangeForm.is_valid():
			# Save changed password
			myPasswordChangeForm.save()
			messages.success( request, "Password has been successfully changed." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.change_password" )
		#else:
			#print "Form is not valid!"
	# Handle GET requests
	elif request.method == "GET":
		myPasswordChangeForm	= MyPasswordChangeForm( request.user )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { "form" : myPasswordChangeForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/change_password.html", variables, context )	


"""
Nintendo Game & Watch Shop > My Account > Address Book

Author(s): Markku Laine
"""
@login_required
def address_book( request ):
	# Handle GET requests
	if request.method == "GET":
		addresses				= Address.objects.filter( user=request.user )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	variables					= { "addresses" : addresses, "first_name" : request.user.first_name, "last_name" : request.user.last_name }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/address_book.html", variables, context )


"""
Nintendo Game & Watch Shop > My Account > Address Book > New Address

Author(s): Markku Laine
"""
@login_required
def address_book_new( request ):
	# Create a new address. Associate the currently logged-in user with the address
	address						= Address()
	address.user				= request.user
	
	# Handle POST requests
	if request.method == "POST":
		addressForm				= AddressForm( data=request.POST, instance=address )

		# Check the validity of the form
		if addressForm.is_valid():
			# Save new address
			addressForm.save()
			messages.success( request, "New address has been successfully saved." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.address_book" )
		#else:
			#print "Form is not valid!"			
	# Handle GET requests
	elif request.method == "GET":
		addressForm				= AddressForm( initial={} )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
		
	variables					= { "form" : addressForm, "first_name" : request.user.first_name, "last_name" : request.user.last_name }
	context						= RequestContext( request )
	#context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/address_book_new.html", variables, context )	


"""
Nintendo Game & Watch Shop > My Account > Address Book > Edit Address

Author(s): Markku Laine
"""
@login_required
def address_book_edit( request, address_id=None ):
	# Retrieve the address. Users are allowed to edit their own addresses only!
	address						= get_object_or_404( Address, pk=address_id, user=request.user )

	# Handle POST requests
	if request.method == "POST":
		addressForm				= AddressForm( data=request.POST, instance=address )

		# Check the validity of the form
		if addressForm.is_valid():
			# Save changed address
			addressForm.save()
			messages.success( request, "Address has been successfully updated." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.address_book" )
		#else:
			#print "Form is not valid!"			
	# Handle GET requests
	elif request.method == "GET":
		addressForm				= AddressForm( instance=address )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
		
	variables					= { "form" : addressForm, "first_name" : request.user.first_name, "last_name" : request.user.last_name }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/address_book_edit.html", variables, context )


"""
Nintendo Game & Watch Shop > My Account > Address Book > Delete Address

Author(s): Markku Laine
"""
@login_required
def address_book_delete( request, address_id=None ):
	# Retrieve user's addresses
	addresses					= Address.objects.filter( user=request.user )
	# Users are not allowed to delete their only address
	if addresses.count() <= 1:
		return redirect( "webshop.views.address_book" )

	# Handle POST requests
	if request.method == "POST":
		# Retrieve the address. Users are allowed to edit their own addresses only!
		address					= get_object_or_404( Address, pk=address_id, user=request.user )
		# Delete address
		address.delete()
		messages.success( request, "Address has been successfully deleted." ) # Levels: info, success, warning, and error
		return redirect( "webshop.views.address_book" )
	# Handle GET requests
	elif request.method == "GET":
		# Retrieve the address. Users are allowed to edit their own addresses only!
		address					= get_object_or_404( Address, pk=address_id, user=request.user )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
		
	variables					= { "address" : address, "first_name" : request.user.first_name, "last_name" : request.user.last_name }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/address_book_delete.html", variables, context )


"""
Nintendo Game & Watch Shop > My Account > Completed Orders

Author(s): Markku Laine
"""
@login_required
def completed_orders( request ):
	# Handle GET requests
	if request.method == "GET":
		# Retrieve completed (paid) orders of the currently logged-in user
		orders					= Order.objects.filter( user=request.user, paid=True )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	variables					= { "orders" : orders }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/completed_orders.html", variables, context )

"""
Author(s): Markku Laine
"""
def about( request ):
	# Handle GET requests
	if request.method == "GET":
		variables					= {}
		context						= RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/about.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Credits

Author(s): Markku Laine
"""

def credits( request ):
	# Handle GET requests
	if request.method == "GET":
		variables                    = {}
		context                        = RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/credits.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

"""
Nintendo Game & Watch Shop > Admin

Author(s): Markku Laine
"""
@login_required
def admin( request ):
	# Redirect user to Home if (s)he is has not access rights
	if not request.user.is_staff:
		return redirect( "webshop.views.home" )

	# Handle GET requests
	if request.method == "GET":
		return redirect( "webshop.views.admin_paid_orders" )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Nintendo Game & Watch Shop > Admin > Paid Orders

Author(s): Markku Laine
"""
@login_required
def admin_paid_orders( request, order_id=None ):
	# Redirect user to Home if (s)he is has not access rights
	if not request.user.is_staff:
		return redirect( "webshop.views.home" )
				
	# Handle POST requests
	if request.method == "POST":
		# Retrieve order id
		order_id				= request.POST.get( "order_id", 0 )
		# Retrieve the order
		order					= get_object_or_404( Order, pk=order_id )
		order.delivered			= True
		order.save()
		# Retrieve paid orders
		orders					= Order.objects.filter( paid=True, delivered=False )
	# Handle GET requests
	elif request.method == "GET":
		# Retrieve paid orders
		orders					= Order.objects.filter( paid=True, delivered=False )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	variables					= { "orders" : orders }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/admin/paid_orders.html", variables, context )


"""
Nintendo Game & Watch Shop > Admin > Delivered Orders

Author(s): Markku Laine
"""
@login_required
def admin_delivered_orders( request ):
	# Redirect user to Home if (s)he is has not access rights
	if not request.user.is_staff:
		return redirect( "webshop.views.home" )
	
	# Handle GET requests
	if request.method == "GET":
		# Retrieve paid & delivered orders
		orders                    = Order.objects.filter( paid=True, delivered=True )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	variables                    = { "orders" : orders }
	context                        = RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/admin/delivered_orders.html", variables, context )


"""
Nintendo Game & Watch Shop > Admin > Statistics

Author(s): Kalle Saila
"""
@login_required
def admin_statistics( request ):
	# Redirect user to Home if (s)he is has not access rights
	if not request.user.is_staff:
		return redirect( "webshop.views.home" )
	
	# Handle GET requests
	if request.method == "GET":
		# Retrieve paid & delivered orders
		orders                    = []
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

	variables                    = { "orders" : orders }
	context                        = RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/admin/statistics.html", variables, context )


"""
Author(s): Juha Loukkola
"""
@login_required
def payment_pay( request ):
	#if request.method == 'POST':
	user = get_object_or_404(User, id=request.user.id)
	sm = request.session.get('shippingMethod')
	shippingMethod = get_object_or_404(ShippingMethod, name=sm)
	
	# create an order from items in the cart
	order = Order(date=datetime.now(), 
				user=user, 
				delivered=False, 
				paid=False,
				shippingMethod=shippingMethod,
				address=user.address_set.all()[0])
	order.save()
	
	# Add orderItems to the order and save them to DB
	orderItems = request.session.get('orderItems')
	for item in orderItems:
		item.order = order
		item.save()
	
	# construct parameters for interfacing the net bank
	pid = order.id
	sid	= 'Disk-kun'
	amount = order.getTotal()
	success_url = request.build_absolute_uri("/webshop/payment/success")
	cancel_url = request.build_absolute_uri("/webshop/payment/cancel") 
	error_url = request.build_absolute_uri("/webshop/payment/error")
	
	# calsulate a cehcksum
	checksumstr = "pid=%s&sid=%s&amount=%s&token=%s"%(pid, sid, amount, secret_key)
	m = md5.new(checksumstr)
	checksum = m.hexdigest()
	
	variables	= { "pid":pid, "sid":sid, "amount":amount, "success_url":success_url, "cancel_url":cancel_url, "error_url":error_url, "checksum":checksum}
	context		= RequestContext( request )
	return render_to_response("webshop/payment/confirm.html", variables, context)
	
"""
Author(s): Juha Loukkola
"""
def payment_confirm( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payment/confirm.html", variables, context )	
	
"""
Author(s): Juha Loukkola
"""
@login_required
def payment_success( request ):
	# Handle GET requests
	if request.method == "GET":

		pid = request.GET.get('pid')
		ref = request.GET.get('ref')
		checksum = request.GET.get('checksum')
		
		# validate checksum
		checksumstr = "pid=%s&ref=%s&token=%s"%(pid, ref, secret_key)
		m = md5.new(checksumstr)
		if checksum == m.hexdigest():
			order = get_object_or_404(Order, id=pid)
			order.paid = True
			order.save()
			if 'orderItems' in request.session:
				del request.session['orderItems']
			if 'shippingMethod' in request.session:
				del request.session['shippingMethod']
			if 'numberOfCartItems' in request.session:
				request.session[ "numberOfCartItems" ]	= 0
			
			variables	= {}
			context		= RequestContext( request )
			return render_to_response( "webshop/payment/success.html", variables, context )
		else:
			context		= RequestContext( request )
			return render_to_response( "webshop/payment/error.html", context )

	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	

	
	
	
"""
Author(s): Juha Loukkola
"""
def payment_cancel( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payment/cancel.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
def payment_error( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payment/error.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
#@login_required
def cart( request ):
	# Handle POST requests
	if request.method == "POST":
		print "Hello"
	# Handle GET requests
	elif request.method == "GET":
		orderItems	= request.session.get('orderItems', [])
		#if 'shippingMethod' in request.session:
		sm			= request.session.get('shippingMethod')
		if sm:
			shippingMethod = get_object_or_404(ShippingMethod, name=sm)
		else:
			request.session['shippingMethod'] = 'Standard'
			shippingMethod = get_object_or_404(ShippingMethod, name='Standard')

		# Calculate subtotal
		subtotal					= 0
		for orderItem in orderItems:
			subtotal				+= ( orderItem.quantity * orderItem.saleItem.price )
		subtotalInEuros				= u"%.2f \u20AC" % subtotal

		shippingMethodInEuros		= u"%.2f \u20AC" % shippingMethod.price
		total						= subtotal + shippingMethod.price
		totalInEuros				= u"%.2f \u20AC" % total
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { 'orderItems': orderItems, 'shippingMethod' : shippingMethod, 'shippingMethodInEuros' : shippingMethodInEuros, "subtotalInEuros" : subtotalInEuros, "totalInEuros" : totalInEuros }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/cart_markku.html", variables, context )


"""
Author(s): Markku Laine
"""
def empty_cart( request ):
	# Handle POST requests
	if request.method == "POST":
		# Empty cart
		request.session[ 'orderItems' ]			= []
		request.session[ "numberOfCartItems" ]	= 0
		return redirect( "webshop.views.cart" )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Author(s): Juha Loukkola
"""
def add_to_cart( request ):
	if request.method == 'POST':
		# Get the cart from the session
		orderItems = request.session.get( 'orderItems', [] )
				
		# Get SaleItem		
		#if 'saleitem_id' in request.POST:
		si_id = request.POST.get('saleitem_id')
		if si_id:
			si = SaleItem.objects.get(id=si_id)
		else:
			return HttpResponseBadRequest()
		# Check if there is allredy similar item in the cart ...
		similarItem = None
		for item in orderItems:
			if item.saleItem.id == si.id:
				similarItem = item
		# ... if similar item exist increase its quantity ...
		if similarItem:
			similarItem.quantity += 1
		# ... else create new item
		else:
			oi = OrderItem()
			oi.quantity = 1
			oi.saleItem = si
			orderItems.append(oi)
		
		# Save the cart into the session
		request.session['orderItems']	= orderItems

		# Calculate the number of cart items
		numberOfCartItems				= 0
		for orderItem in orderItems:
			numberOfCartItems	+= orderItem.quantity
		request.session[ "numberOfCartItems" ]	= numberOfCartItems

		# Handle Ajax request
		if request.is_ajax():
			# Return the number of cart items for updating the cart items number in the navigation
			my_json = json.dumps( { "numberOfCartItems" : numberOfCartItems } )
			return HttpResponse( my_json, mimetype="application/json" )
		# Handle normal request
		else:
			next		= request.POST.get( "next", reverse( "webshop.views.cart" ) )
			return redirect( next )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )

"""
Author(s): Juha Loukkola
"""
def update_cart( request ):
	#if request.is_ajax():
	if request.method == 'POST':				
		# Get the cart
#		orderItems = request.session.get('orderItems', [])					
#		for item in orderItems:
#			item_quantity = int(request.POST.get(item.saleItem.id))
#			item.quantity = item_quantity
		
		# update the shipping method
		if 'shipping_method' in request.POST:
			request.session['shippingMethod'] = request.POST.get('shipping_method')
			return redirect( "webshop.views.cart" )
		else:
			return HttpResponseBadRequest()
	else:
		return HttpResponseBadRequest()

"""
def add_to_cart( request ):
	#if request.is_ajax():
	if request.method == 'POST':
		cart = request.session.get( 'cart' )
		# If this is the first time the cart is refered during this session
		if cart == None:			
			if request.user.is_authenticated():
				user = get_object_or_404(User, id=request.user.id)
				# If the user has unfinished cart from previous session then get it ...
				cart = user.order_set.filter(paid=False)	
				# ... else create new one
				if cart == None:
					cart = Order()
					cart.user = user
					cart.date = datetime.now()
					cart.shipingmethod = None
					cart.paid = False
					cart.delivered = False
					cart.save()
			# If the user is not authenticated then just create a cart
			else:
				cart = Order()
				cart.user = get_object_or_404(User, username='anonymous')
				cart.date = datetime.now()
				cart.shipingmethod = ShipingMethod()
				cart.paid = False
				cart.delivered = False
				cart.save()
						
			request.session['cart'] = cart
	
		# Get SaleItem		
		si_id = request.POST.get('saleitem_id')
		si = SaleItem.objects.get(id=si_id)
		
		# Create a new OrderItem and add it into the cart		
		oi = OrderItem()
		oi.saleItem=si
		oi.order=cart
		oi.quantity=1
		oi.save()
		
		variables	= {}
		context		= RequestContext( request )
		return render_to_response( "webshop/cart.html", variables, context )
	else:
		return HttpResponseBadRequest()
"""

"""
Author(s): Kalle Saila
"""
### AJAX ###
def rating( request, product_id ):
	if request.is_ajax():
		if request.method == 'POST':
			try:
				product	= Product.objects.get(id=product_id)
				try:
					rate	= Rating.objects.get(product=product, user=request.user)
					newrate = request.POST['rate']
					rate.rate = newrate
					rate.save()
					average = product.average()
					count = product.rating_set.count()
					my_json = json.dumps({'average':average, 'count':count})
					return HttpResponse(my_json, mimetype="application/json")
				except Rating.DoesNotExist:
					rate = Rating()
					rate.rate = request.POST['rate']
					rate.user = request.user
					rate.product = product
					rate.save()
					average = product.average()
					count = product.rating_set.count()
					my_json = json.dumps({'average':average, 'count':count})
					return HttpResponse(my_json, mimetype="application/json")
			except Product.DoesNotExist:
				my_json = json.dumps({'error':'product not found'})
				return HttpResponse(my_json, mimetype="application/json")
		else:
			try:
				product	= Product.objects.get(id=product_id)
				average = product.average()
				count = product.rating_set.count()
				my_json = json.dumps({'average':average, 'count':count})
				return HttpResponse(my_json, mimetype="application/json")
			except Product.DoesNotExist:
				my_json = json.dumps({'error':'product not found'})
				return HttpResponse(my_json, mimetype="application/json")
	else:
		my_json = json.dumps({})
		return HttpResponse(my_json, mimetype="application/json")
	
def comment( request, product_id ):
	if request.is_ajax():
		if request.method == 'POST':
			try:
				product	= Product.objects.get(id=product_id)
				comment = Comment()
				comment.user = request.user
				if request.POST['commentsOn'] != 'None':
					commentsOn = Comment.objects.get(id=request.POST['commentsOn'])
					comment.commentsOn = commentsOn
				comment.contents = request.POST['comment']
				comment.product = product
				comment.published = datetime.today()
				comment.save()
				my_json = json.dumps({'id':comment.id, 'commentsOn':request.POST['commentsOn'], 'published':comment.published.__str__(), 'user': comment.user.username, 'admin': comment.user.is_staff})
				return HttpResponse(my_json, mimetype="application/json")
			except Product.DoesNotExist:
				my_json = json.dumps({'error':'product not found'})
				return HttpResponse(my_json, mimetype="application/json")
		else:
			try:
				my_json = json.dumps({})
				return HttpResponse(my_json, mimetype="application/json")
			except Product.DoesNotExist:
				my_json = json.dumps({'error':'product not found'})
				return HttpResponse(my_json, mimetype="application/json")
	else:
		my_json = json.dumps({})
		return HttpResponse(my_json, mimetype="application/json")
	
def ajaxproducts( request ):
	if request.is_ajax():
		#my_json = json.dumps(Product.objects.all(), cls=DjangoJSONEncoder)
		my_list = []
		for p in Product.objects.all():
			temp_dict = {}
			temp_dict["id"] = p.id
			temp_dict["type"] = p.type.id
			temp_dict["label"] = p.title
			my_list.append(temp_dict)
			#my_list.append("{\"id\":" + str(p.id) + ", \"type\":" + str(p.type.id) + ", \"label\":\"" + p.title+"\"}")
		my_json = json.dumps(my_list)
		return HttpResponse(my_json, mimetype="application/json")
	else:
		#my_json = json.dumps(Product.objects.all(), cls=DjangoJSONEncoder)
		#my_json = json.dumps(json.loads(serialize('json', Product.objects.all())))
		#return HttpResponse(my_json, mimetype="application/json")
		my_list = []
		for p in Product.objects.all():
			temp_dict = {}
			temp_dict["id"] = p.id
			temp_dict["type"] = p.type.id
			temp_dict["label"] = p.title
			my_list.append(temp_dict)
			#my_list.append("{\"id\":" + str(p.id) + ", \"type\":" + str(p.type.id) + ", \"label\":\"" + p.title+"\"}")
		my_json = json.dumps(my_list)
		return HttpResponse(my_json, mimetype="application/json")
	
def ajaxstatisticscommentcount( request ):
	my_list = []
	for p in Product.objects.all():
		if p.comment_set.count() > 0:
			temp_dict = {}
			temp_dict["name"] = p.title
			temp_dict["y"] = p.comment_set.count()
			my_list.append(temp_dict)
	my_json = json.dumps(my_list)
	return HttpResponse(my_json, mimetype="application/json")

def productview( request ):
	my_list = []
	for s in Statistic.objects.all():
		temp_dict = {}
		temp_dict["name"] = s.product.title
		temp_dict["y"] = s.numberOfViews
		my_list.append(temp_dict)
			
	my_json = json.dumps(my_list)
	return HttpResponse(my_json, mimetype="application/json")

def addproductview( request, product_id ):
	try:
		product = Product.objects.get(id=product_id)
		try:
			stat = Statistic.objects.get(product=product)
			stat.numberOfViews = stat.numberOfViews + 1
			stat.save() 
		except Statistic.DoesNotExist:
			stat = Statistic()
			stat.numberOfViews = 1
			stat.product = product
			stat.save()
	except Product.DoesNotExist:
		my_json = json.dumps("{}")
		return HttpResponse(my_json, mimetype="application/json")
	
	my_json = json.dumps("{}")
	return HttpResponse(my_json, mimetype="application/json")

def commentdelete( request, comment_id ):
	if not request.user.is_staff:
		my_json = json.dumps({'error':'not authorized'})
		return HttpResponse(my_json, mimetype="application/json")
	try:
		comment = Comment.objects.get(id=comment_id)
		if Comment.objects.filter(commentsOn=comment).count() > 0:
			my_json = json.dumps({'error':'comment not removable'})
			return HttpResponse(my_json, mimetype="application/json")
		comment.delete()
		my_json = json.dumps("{}")
		return HttpResponse(my_json, mimetype="application/json")
	except Comment.DoesNotExist:
		my_json = json.dumps({'error':'comment not found'})
		return HttpResponse(my_json, mimetype="application/json")
	
	my_json = json.dumps("{}")
	return HttpResponse(my_json, mimetype="application/json")