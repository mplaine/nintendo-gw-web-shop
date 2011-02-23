# Create your views here.
from django.core.urlresolvers import reverse
#from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from webshop.forms import ProductForm
from webshop.models import SaleItem, Product, Type
from django.template.loader import get_template
from django.template.context import Context
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

#from django.http import HttpResponse
#from django.template import Context, loader
#from polls.models import Choice, Poll


def home( request ):
	errorMessage				= ""
	username					= ""
	next						= "/webshop/home/"
	
	if request.method == "POST":
		username				= request.POST.get( "username", "" )
		password				= request.POST.get( "password", "" )
		user					= authenticate( username=username, password=password )

		if user is not None:
			if user.is_active:
				# Login the user
				auth_login( request, user )
				return HttpResponseRedirect( "/webshop/home/" )
			else:
				errorMessage	= "Your account is not active, please contact the site administrator."
		else:
			errorMessage		= "Username and/or password was incorrect"
#	else:
		# Handle the GET request
	
	types						= Type.objects.all().order_by( "name" )
	variables					= { "errorMessage" : errorMessage, "username" : username, "next" : next, "types" : types }
	context						= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/index.html", variables, context )
#	types		= Type.objects.all().order_by( "name" )
#	variables	= { "types" : types }
#	context		= RequestContext( request )
#	return render_to_response( "webshop/index.html", variables, context )

def category( request, type_id ):
	type		= get_object_or_404( Type, id=type_id )
	variables	= { "type" : type }
	context		= RequestContext( request )
	return render_to_response( "webshop/category.html", variables, context )

def register( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/register.html", variables, context )

def logout( request ):
	auth_logout( request )
	return HttpResponseRedirect( "/webshop/home/" )

def login( request ):
	errorMessage				= ""
	username					= ""
	next						= "/webshop/home/"
	
	if request.method == "POST":
		username				= request.POST.get( "username", "" )
		password				= request.POST.get( "password", "" )
		user					= authenticate( username=username, password=password )

		if user is not None:
			if user.is_active:
				# Login the user
				auth_login( request, user )
				return HttpResponseRedirect( "/webshop/home/" )
			else:
				errorMessage	= "Your account is not active, please contact the site administrator."
		else:
			errorMessage		= "Username and/or password was incorrect"
#	else:
		# Handle the GET request
	
	variables			= { "errorMessage" : errorMessage, "username" : username, "next" : next }
	context				= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/login.html", variables, context )

def login_old2( request ):
	state	= "Please log in below"
	username	= ""
	password	= ""
	if request.POST:
		username	= request.POST.get( "username" )
		password	= request.POST.get( "password" )
		
		user		= authenticate( username=username, password=password )
		if user is not None:
			if user.is_active:
				auth_login( request, user )
				state	= "You are successfully logged in!"
				return HttpResponseRedirect( '/webshop/home/' )
			else:
				state	= "Your account is not active, please contact the site admin."
				return HttpResponseRedirect( '/webshop/home/' )
		else:
			state		= "Your username and/or password were incorrect."

	authenticationForm	= AuthenticationForm()
	variables			= RequestContext( request, { 'form' : authenticationForm })
	variables.update( csrf( request ) )
	return render_to_response( "webshop/login.html", { "state": state, "username": username }, variables )
	
def login_old( request ):
	username	= request.POST[ "username" ]
	password	= request.POST[ "password" ]
	user		= authenticate( username=username, password=password )
	if user is not None:
		if user.is_active:
			print "You provided a correct username and password!"
			#login( request, user )
			# Redirect to a success page
		else:
			print "Your account has been disabled!"
			# Redirect to a disabled account
	else:
		print "Your username and password were incorrect."
		# Return an invalid login error page

def search( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/search.html", variables, context )