# Create your views here.
from django.core.urlresolvers import reverse
#from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from webshop.forms import ProductForm
from webshop.models import ProductDetails, Product, Type
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

def category( request ):
	return render_to_response( 'webshop/category.html', context_instance = RequestContext( request ) )

def register( request ):
	return render_to_response( 'webshop/register.html', context_instance = RequestContext( request ) )

def search( request ):
	return render_to_response( 'webshop/search.html', context_instance = RequestContext( request ) )

def add_product( request ):
	if request.method == 'POST': 
		form = ProductForm(request.POST)
		
		if form.is_valid(): 
			productDetails = ProductDetails(name = form.cleaned_data['name'], price = form.cleaned_data['price'], quantity = form.cleaned_data['quantity'], picture = u'http://www.kuva.fi')
			productDetails.save()
			product = Product(details = productDetails, numOfComments = 0, numOfViews = 0, numOfPurchases = 0)
			product.save()
			#return HttpResponseRedirect('webshop/product/%d/' % (product.pk))
			return HttpResponseRedirect('/webshop/products/')
		else:
			variables = RequestContext(request, { 'form' : form })
			variables.update(csrf(request))
			return render_to_response( 'webshop/add_product.html', variables )
	else: 
		form = ProductForm()
		variables = RequestContext(request, { 'form' : form })
		variables.update(csrf(request))
		return render_to_response( 'webshop/add_product.html', variables )
	
def view_products( request ):
	products = ProductDetails.objects.all()  
	template = get_template("webshop/products.html")
	variables = Context( {'products' : products })
	return HttpResponse( template.render(variables) )