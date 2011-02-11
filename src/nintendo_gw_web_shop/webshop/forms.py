from django import forms 
from django.forms import widgets

class ProductForm(forms.Form): 
    name        = forms.CharField(label=u'Name', max_length=50)
    price       = forms.DecimalField(label=u'Price', decimal_places=2, max_digits=6)
    quantity    = forms.IntegerField(label=u'Quantity')
