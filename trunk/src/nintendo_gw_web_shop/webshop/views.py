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

#from django.http import HttpResponse
#from django.template import Context, loader
#from polls.models import Choice, Poll


def home( request ):
	types = Type.objects.all().order_by('name')
	template = get_template('webshop/index.html')
	variables = Context({'types':types})
	
	return HttpResponse(template.render(variables))
	#return render_to_response( 'webshop/index.html', context_instance = RequestContext( request ) )

def category( request, type_id ):
	type = get_object_or_404(Type, id=type_id)
	template = get_template('webshop/category.html')
	variables = Context({'type':type})
	return HttpResponse(template.render(variables))

def register( request ):
	return render_to_response( 'webshop/register.html', context_instance = RequestContext( request ) )

def search( request ):
	return render_to_response( 'webshop/search.html', context_instance = RequestContext( request ) )