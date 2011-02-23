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
	if request.method == "POST":
		form			= AuthenticationForm( data=request.POST )
		if form.is_valid():
			username	= form.cleaned_data[ "username" ]
			password	= form.cleaned_data[ "password" ]
			user		= authenticate( username=username, password=password )
			auth_login( request, user )
			return HttpResponseRedirect( "/webshop/home/" )
		#else:
			#print "Form is not valid!"
	else:
		form			= AuthenticationForm( initial={ "username" : "username", "password" : "password" } )	
	
	next				= "/webshop/home/"
	types				= Type.objects.all().order_by( "name" )
	variables			= { "form" : form, "next" : next, "types" : types }
	context				= RequestContext( request )
	context.update( csrf( request ) )
	return render_to_response( "webshop/index.html", variables, context )

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

def search( request ):
	variables	= {}
	context		= RequestContext( request )
	return render_to_response( "webshop/search.html", variables, context )