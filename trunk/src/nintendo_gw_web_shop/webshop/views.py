from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from webshop.forms import ProductForm, MyUserChangeForm
from webshop.models import SaleItem, Product, Type
from django.template.loader import get_template
from django.template.context import Context
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


def home( request ):
	types						= Type.objects.all().order_by( "name" )
	variables					= { "types" : types }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/index.html", variables, context )

def login( request ):
	if request.method == "POST":
		authenticationForm		= AuthenticationForm( data=request.POST )
		if authenticationForm.is_valid():
			username			= authenticationForm.cleaned_data.get( "username", "" )
			password			= authenticationForm.cleaned_data.get( "password", "" )
			user				= authenticate( username=username, password=password )
			auth_login( request, user )
			next				= request.POST.get( "next", reverse( "webshop.views.home" ) )
			return redirect( next )
		#else:
			#print "Form is not valid!"
	else:
		authenticationForm		= AuthenticationForm( initial={ "username" : "", "password" : "" } )	
	
	next						= request.META.get( "HTTP_REFERER", reverse( "webshop.views.home" ) )
	variables					= { "form" : authenticationForm, "next" : next }
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
		return redirect( "webshop.views.account" )
		
	if request.method == "POST":
		userCreationForm		= UserCreationForm( data=request.POST )
		if userCreationForm.is_valid():
			userCreationForm.save()
			return redirect( "webshop.views.home" )
		#else:
			#print "Form is not valid!"
	else:
		userCreationForm		= UserCreationForm()
	
	variables					= { "userCreationForm" : userCreationForm }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/register.html", variables, context )

def account( request ):
	if request.method == "POST":
		myUserChangeForm		= MyUserChangeForm( data=request.POST, instance=request.user )
		if myUserChangeForm.is_valid():
			myUserChangeForm.save()
			return redirect( "webshop.views.home" )
		#else:
			#print "Form is not valid!"
	else:
		if request.user.is_authenticated():
			myUserChangeForm	= MyUserChangeForm( instance=request.user )
		else:
			myUserChangeForm	= MyUserChangeForm()
	
	variables					= { "myUserChangeForm" : myUserChangeForm }
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