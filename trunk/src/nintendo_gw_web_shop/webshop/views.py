from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from webshop.forms import ProductForm, MyUserCreationForm, MyAuthenticationForm, MyUserChangeForm, MyPasswordResetForm, MyPasswordChangeForm
from webshop.models import SaleItem, Product, Type
from django.template.loader import get_template
from django.template.context import Context
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import password_reset


def root( request ):
	return redirect( "webshop.views.home" )

def home( request ):
	types						= Type.objects.all().order_by( "name" )
	variables					= { "types" : types }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/index.html", variables, context )

def login( request ):
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	if request.method == "POST":
		myAuthenticationForm	= MyAuthenticationForm( data=request.POST )
		if myAuthenticationForm.is_valid():
			username			= myAuthenticationForm.cleaned_data.get( "username", "" )
			password			= myAuthenticationForm.cleaned_data.get( "password", "" )
			user				= authenticate( username=username, password=password )
			auth_login( request, user )
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			return redirect( next )
		#else:
			#print "Form is not valid!"
	else:
		myAuthenticationForm	= MyAuthenticationForm( initial={} )	
	
	next						= request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) ) # After a successful login, redirect the user to the page (s)he came from
	variables					= { "form" : myAuthenticationForm, "next" : next }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/login.html", variables, context )	

#def my_password_reset(request, template_name='path/to/my/template'):
def my_password_reset(request):
	return password_reset( request )

# Not working
def forgot_your_password( request ):
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	if request.method == "POST":
		myPasswordResetForm		= MyPasswordResetForm( data=request.POST )
		if myPasswordResetForm.is_valid():
			# Diabled
			#myPasswordResetForm.save()
			messages.success( request, "Password has been successfully reset (not implemented)." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.forgot_your_password" )
#			username			= myAuthenticationForm.cleaned_data.get( "username", "" )
#			password			= myAuthenticationForm.cleaned_data.get( "password", "" )
#			user				= authenticate( username=username, password=password )
#			auth_login( request, user )
#			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
#			return redirect( next )
		#else:
			#print "Form is not valid!"
	else:
		myPasswordResetForm		= MyPasswordResetForm( initial={} )	
	
	variables					= { "form" : myPasswordResetForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/forgot_your_password.html", variables, context )	

def change_password( request ):
	if not request.user.is_authenticated():
		return redirect( "webshop.views.home" )

	if request.method == "POST":
		myPasswordChangeForm	= MyPasswordChangeForm( data=request.POST, user=request.user )
		if myPasswordChangeForm.is_valid():
			myPasswordChangeForm.save()
			messages.success( request, "Password has been successfully changed." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.change_password" )
		#else:
			#print "Form is not valid!"
	else:
		myPasswordChangeForm	= MyPasswordChangeForm( request.user )
	
	variables					= { "form" : myPasswordChangeForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/change_password.html", variables, context )	

def category( request, type_id ):
	type						= get_object_or_404( Type, id=type_id )
	variables					= { "type" : type }
	context						= RequestContext( request )
	return render_to_response( "webshop/category.html", variables, context )

def register( request ):
	if request.user.is_authenticated():
		return redirect( "webshop.views.home" )
		
	if request.method == "POST":
		myUserCreationForm		= MyUserCreationForm( data=request.POST )
		if myUserCreationForm.is_valid():
			user				= myUserCreationForm.save()
			# Automatically login the user after successful registration
			user.backend		= "django.contrib.auth.backends.ModelBackend"
			auth_login( request, user )
			return redirect( "webshop.views.home" )
		#else:
			#print "Form is not valid!"
	else:
		myUserCreationForm		= MyUserCreationForm( initial={} )
	
	variables					= { "form" : myUserCreationForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/register.html", variables, context )

def myaccount( request ):
	return redirect( "webshop.views.account_details" )

def account_details( request ):
	if not request.user.is_authenticated():
		return redirect( "webshop.views.home" )	
	
	if request.method == "POST":
		myUserChangeForm		= MyUserChangeForm( data=request.POST, instance=request.user )
		if myUserChangeForm.is_valid():
			myUserChangeForm.save()
			messages.success( request, "Account details have been successfully updated." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.account_details" )
		#else:
			#print "Form is not valid!"
	else:
		myUserChangeForm		= MyUserChangeForm( instance=request.user )
	
	variables					= { "form" : myUserChangeForm, "username_label" : "Username:", "username" : request.user.username }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/account_details.html", variables, context )

def address_book( request ):
	if not request.user.is_authenticated():
		return redirect( "webshop.views.home" )	
	
	variables					= {}
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/address_book.html", variables, context )

def completed_orders( request ):
	if not request.user.is_authenticated():
		return redirect( "webshop.views.home" )	
	
	variables					= {}
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/myaccount/completed_orders.html", variables, context )

def logout( request ):
	auth_logout( request )
	return redirect( "webshop.views.home" )

def search( request ):
	variables					= {}
	context						= RequestContext( request )
	return redirect( "webshop.views.home" )

def about( request ):
	variables					= {}
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/about.html", variables, context )

def credits( request ):
	variables					= {}
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/credits.html", variables, context )

def payment_pay( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payement_pay.html", variables, context )
	
def payment_success( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/payement_success.html", variables, context )
	
def payment_cancel( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/cart.html", variables, context )
	
def payment_error( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/error.html", variables, context )
	
def cart( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/cart.html", variables, context )

