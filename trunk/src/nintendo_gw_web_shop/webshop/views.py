from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from webshop.forms import ProductForm, MyUserCreationForm, MyAuthenticationForm, MyUserChangeForm
from webshop.models import SaleItem, Product, Type
from django.template.loader import get_template
from django.template.context import Context
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages


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
		myAuthenticationForm	= MyAuthenticationForm( initial={ "username" : "", "password" : "" } )	
	
	next						= request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) ) # After a successful login, redirect the user to the page (s)he came from
	variables					= { "form" : myAuthenticationForm, "next" : next }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/login.html", variables, context )	

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
		myUserCreationForm		= MyUserCreationForm( initial={ "username" : "", "password1" : "", "password2" : "" } )
	
	variables					= { "form" : myUserCreationForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/register.html", variables, context )

def account( request ):
	if not request.user.is_authenticated():
		return redirect( "webshop.views.home" )	
	
	if request.method == "POST":
		myUserChangeForm		= MyUserChangeForm( data=request.POST, instance=request.user )
		if myUserChangeForm.is_valid():
			myUserChangeForm.save()
			messages.success( request, "Profile has been successfully updated." ) # Levels: info, success, warning, and error
			return redirect( "webshop.views.account" )
		#else:
			#print "Form is not valid!"
	else:
		myUserChangeForm		= MyUserChangeForm( instance=request.user )
	
	variables					= { "form" : myUserChangeForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/account.html", variables, context )

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