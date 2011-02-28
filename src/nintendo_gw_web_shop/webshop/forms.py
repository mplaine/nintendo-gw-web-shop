from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import widgets

class ProductForm(forms.Form): 
    name        = forms.CharField(label=u'Name', max_length=50)
    price       = forms.DecimalField(label=u'Price', decimal_places=2, max_digits=6)
    quantity    = forms.IntegerField(label=u'Quantity')

class MyAuthenticationForm( AuthenticationForm ):
    username_label          = "Username"
    username_max_length     = 30
    password_label          = "Password"
    password_max_length     = 128
    username                = forms.CharField( label="%s:" % username_label, max_length="%d" % username_max_length, error_messages={ "required" : "%s is required." % username_label, "max_length" : "%s is too long, maximum length is %d." % ( username_label, username_max_length ) } )
    password                = forms.CharField( label="%s:" % password_label, max_length="%d" % password_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password_label, "max_length" : "%s is too long, maximum length is %d." % ( password_label, password_max_length ) })

class MyUserCreationForm( UserCreationForm ):
    first_name_label        = "First name"
    first_name_max_length   = 30
    last_name_label         = "Last name"
    last_name_max_length    = 30
    username_label          = "Username"
    username_max_length     = 30
    password1_label         = "Password"
    password1_max_length    = 128
    password2_label         = "Confirm password"
    password2_max_length    = 128
    email_label             = "E-mail address"
    email_max_length        = 128
    first_name              = forms.CharField( label="%s:" % first_name_label, max_length="%d" % first_name_max_length, error_messages={ "required" : "%s is required." % first_name_label, "max_length" : "%s is too long, maximum length is %d." % ( first_name_label, first_name_max_length ) } )
    last_name               = forms.CharField( label="%s:" % last_name_label, max_length="%d" % last_name_max_length, error_messages={ "required" : "%s is required." % last_name_label, "max_length" : "%s is too long, maximum length is %d." % ( last_name_label, last_name_max_length ) } )
    username                = forms.RegexField( label="%s:" % username_label, max_length="%d" % username_max_length, regex=r"^[\w.@+-]+$", error_messages={ "required" : "%s is required." % username_label, "max_length" : "%s is too long, maximum length is %d." % ( username_label, username_max_length ), "invalid": "%s may contain only letters, numbers and @/./+/-/_ characters." % username_label } )
    password1               = forms.CharField( label="%s:" % password1_label, max_length="%d" % password1_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password1_label, "max_length" : "%s is too long, maximum length is %d." % ( password1_label, password1_max_length ) })
    password2               = forms.CharField( label="%s:" % password2_label, max_length="%d" % password2_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password2_label, "max_length" : "%s is too long, maximum length is %d." % ( password2_label, password2_max_length ) })
    email                   = forms.EmailField( label="%s:" % email_label, max_length="%d" % email_max_length, error_messages={ "required" : "%s is required." % email_label, "max_length" : "%s is too long, maximum length is %d." % ( email_label, email_max_length ) } )

    class Meta( UserCreationForm.Meta ):
        fields  = ( "first_name", "last_name", "username", "password1", "password2", "email" )
    
class MyUserChangeForm( UserChangeForm ):
    first_name_label        = "First name"
    first_name_max_length   = 30
    last_name_label         = "Last name"
    last_name_max_length    = 30
    email_label             = "E-mail address"
    email_max_length        = 128
    first_name              = forms.CharField( label="%s:" % first_name_label, max_length="%d" % first_name_max_length, error_messages={ "required" : "%s is required." % first_name_label, "max_length" : "%s is too long, maximum length is %d." % ( first_name_label, first_name_max_length ) } )
    last_name               = forms.CharField( label="%s:" % last_name_label, max_length="%d" % last_name_max_length, error_messages={ "required" : "%s is required." % last_name_label, "max_length" : "%s is too long, maximum length is %d." % ( last_name_label, last_name_max_length ) } )
    email                   = forms.EmailField( label="%s:" % email_label, max_length="%d" % email_max_length, error_messages={ "required" : "%s is required." % email_label, "max_length" : "%s is too long, maximum length is %d." % ( email_label, email_max_length ) } )
    
    class Meta( UserChangeForm.Meta ):
        fields  = ( "first_name", "last_name", "email" )
        
    def __init__( self, *args, **kwargs ):
        super( MyUserChangeForm, self ).__init__( *args, **kwargs )
        del self.fields[ "username" ] # This is a declared field we really want to be removed from the form to be rendered