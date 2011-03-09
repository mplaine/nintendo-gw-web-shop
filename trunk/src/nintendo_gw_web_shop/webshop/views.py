from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from webshop.forms import MyUserCreationForm, MyAuthenticationForm, MyUserChangeForm, MyPasswordResetForm, MyPasswordChangeForm, AddressForm
from webshop.models import Product, Type, Address, Order, Rating
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.views import password_reset
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required


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
		return redirect( "webshop.views.home" )
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

	# Handle POST requests		
	if request.method == "POST":
		myUserCreationForm		= MyUserCreationForm( data=request.POST )

		# Check the validity of the form
		if myUserCreationForm.is_valid():
			user				= myUserCreationForm.save()
			# Automatically login the user after successful registration
			user.backend		= "django.contrib.auth.backends.ModelBackend"
			auth_login( request, user )
			# After a successful registration, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			return redirect( next )
		else:
			#print "Form is not valid!"
			# After a failed registration, redirect the user to the page (s)he came from based on 1) next URL parameter and 2) default to home
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
	# Handle GET requests
	elif request.method == "GET":
		myUserCreationForm		= MyUserCreationForm( initial={} )
		# After registration, redirect the user to the page (s)he came from based on 1) next URL parameter, 2) HTTP REFERER, and 3) default to home
		next					= request.GET.get( "next", request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) ) )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )
	
	variables					= { "form" : myUserCreationForm, "next" : next }
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
				
	variables					= { "form" : myAuthenticationForm, "next" : next }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/login.html", variables, context )	



"""
Nintendo Game & Watch Shop > Login > Forgot Your Password?

Status: Partly in use!!!

Author(s): Markku Laine
"""
def forgot_your_password( request ):
	# Redirect user to Home if (s)he is currently logged in
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	# Handle POST requests
	if request.method == "POST":
		myPasswordResetForm		= MyPasswordResetForm( data=request.POST )
		if myPasswordResetForm.is_valid():
			# Diabled
			#myPasswordResetForm.save()
			messages.success( request, "Password has been successfully reset (not implemented)." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.forgot_your_password" )
			#username			= myAuthenticationForm.cleaned_data.get( "username", "" )
			#password			= myAuthenticationForm.cleaned_data.get( "password", "" )
			#user				= authenticate( username=username, password=password )
			#auth_login( request, user )
			#next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			#return redirect( next )
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
	return render_to_response( "webshop/forgot_your_password.html", variables, context )	


"""
Nintendo Game & Watch Shop > Login > Forgot Your Password? > Password Reset

Status: Not in use!!!

Author(s): Markku Laine
"""
def my_password_reset(request):
	#def my_password_reset(request, template_name='path/to/my/template'):
	return password_reset( request )


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
	# Retrieve the address. Users are allowed to edit their own addresses only!
	address						= get_object_or_404( Address, pk=address_id, user=request.user )

	# Handle POST requests
	if request.method == "POST":
		# Delete address
		address.delete()
		messages.success( request, "Address has been successfully deleted." ) # Levels: info, success, warning, and error
		return redirect( "webshop.views.address_book" )
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
Nintendo Game & Watch Shop > About

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
		variables					= {}
		context						= RequestContext( request )
		context.update( csrf( request ) )
		return render_to_response( "webshop/credits.html", variables, context )
	# Handle other requests
	else:
		raise Http404( "%s method is not supported." % request.method )


"""
Author(s): Juha Loukkola
"""
def payment_pay( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payement_pay.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
def payment_success( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payement_success.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
def payment_cancel( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/cart.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
def payment_error( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/error.html", variables, context )
	
	
"""
Author(s): Juha Loukkola
"""
def cart( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/cart.html", variables, context )


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