from django import forms 
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import widgets

class ProductForm(forms.Form): 
    name        = forms.CharField(label=u'Name', max_length=50)
    price       = forms.DecimalField(label=u'Price', decimal_places=2, max_digits=6)
    quantity    = forms.IntegerField(label=u'Quantity')

class MyUserChangeForm( UserChangeForm ):
    class Meta( UserChangeForm.Meta ):
        fields  = ( "first_name", "last_name", "email" )
    
    def __init__( self, *args, **kwargs ):
        super( MyUserChangeForm, self ).__init__( *args, **kwargs )
        del self.fields[ "username" ] # This is a declared field we really want to be removed from the form to be rendered