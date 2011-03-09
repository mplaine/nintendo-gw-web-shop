from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, UserChangeForm, PasswordChangeForm
from django.forms import ModelForm
from webshop.models import Address


"""
Address form.

Author(s): Markku Laine
"""
class AddressForm( ModelForm ):
    class Meta:
        model                   = Address
        exclude                 = ( "user" )

    def __init__( self, *args, **kwargs ):
        super( AddressForm, self ).__init__( *args, **kwargs )
        # Override default error messages
        self.fields[ "streetAddressLine1" ].error_messages = { "required": "%s is required." % self.fields[ "streetAddressLine1" ].label, "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "streetAddressLine1" ].label,self.fields[ "streetAddressLine1" ].max_length ) }
        self.fields[ "streetAddressLine2" ].error_messages = { "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "streetAddressLine2" ].label,self.fields[ "streetAddressLine2" ].max_length ) }
        self.fields[ "zipCode" ].error_messages = { "required": "%s is required." % self.fields[ "zipCode" ].label, "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "zipCode" ].label,self.fields[ "zipCode" ].max_length ) }
        self.fields[ "city" ].error_messages = { "required": "%s is required." % self.fields[ "city" ].label, "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "city" ].label,self.fields[ "city" ].max_length ) }
        self.fields[ "state" ].error_messages = { "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "state" ].label,self.fields[ "state" ].max_length ) }
        self.fields[ "country" ].error_messages = { "required": "%s is required." % self.fields[ "country" ].label, "max_length" : "%s is too long, maximum length is %d." % ( self.fields[ "country" ].label,self.fields[ "country" ].max_length ) }
        self.fields[ "country" ].widget.attrs[ "readonly" ]  = True


"""
Authentication (login) form.

Author(s): Markku Laine
"""
class MyAuthenticationForm( AuthenticationForm ):
    username_label              = "Username"
    username_max_length         = 30
    password_label              = "Password"
    password_max_length         = 128
    username                    = forms.CharField( label="%s" % username_label, max_length="%d" % username_max_length, error_messages={ "required" : "%s is required." % username_label, "max_length" : "%s is too long, maximum length is %d." % ( username_label, username_max_length ) } )
    password                    = forms.CharField( label="%s" % password_label, max_length="%d" % password_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password_label, "max_length" : "%s is too long, maximum length is %d." % ( password_label, password_max_length ) })


"""
Password reset (forgot your password?) form.

Author(s): Markku Laine
"""
class MyPasswordResetForm( PasswordResetForm ):
    email_label                 = "E-mail address"
    email_max_length            = 128
    email                       = forms.EmailField( label="%s" % email_label, max_length="%d" % email_max_length, error_messages={ "required" : "%s is required." % email_label, "max_length" : "%s is too long, maximum length is %d." % ( email_label, email_max_length ) } )


"""
Password change (change password) form.

Author(s): Markku Laine
"""
class MyPasswordChangeForm( PasswordChangeForm ):
    old_password_label          = "Old password"
    old_password_max_length     = 128
    new_password1_label         = "New password"
    new_password1_max_length    = 128
    new_password2_label         = "Confirm new password"
    new_password2_max_length    = 128
    old_password                = forms.CharField( label="%s" % old_password_label, max_length="%d" % old_password_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % old_password_label, "max_length" : "%s is too long, maximum length is %d." % ( old_password_label, old_password_max_length ) })
    new_password1               = forms.CharField( label="%s" % new_password1_label, max_length="%d" % new_password1_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % new_password1_label, "max_length" : "%s is too long, maximum length is %d." % ( new_password1_label, new_password1_max_length ) })
    new_password2               = forms.CharField( label="%s" % new_password2_label, max_length="%d" % new_password2_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % new_password2_label, "max_length" : "%s is too long, maximum length is %d." % ( new_password2_label, new_password2_max_length ) })


"""
User creation (register) form.

Author(s): Markku Laine
"""
class MyUserCreationForm( UserCreationForm ):
    first_name_label            = "First name"
    first_name_max_length       = 30
    last_name_label             = "Last name"
    last_name_max_length        = 30
    username_label              = "Username"
    username_max_length         = 30
    password1_label             = "Password"
    password1_max_length        = 128
    password2_label             = "Confirm password"
    password2_max_length        = 128
    email_label                 = "E-mail address"
    email_max_length            = 128
    first_name                  = forms.CharField( label="%s" % first_name_label, max_length="%d" % first_name_max_length, error_messages={ "required" : "%s is required." % first_name_label, "max_length" : "%s is too long, maximum length is %d." % ( first_name_label, first_name_max_length ) } )
    last_name                   = forms.CharField( label="%s" % last_name_label, max_length="%d" % last_name_max_length, error_messages={ "required" : "%s is required." % last_name_label, "max_length" : "%s is too long, maximum length is %d." % ( last_name_label, last_name_max_length ) } )
    username                    = forms.RegexField( label="%s" % username_label, max_length="%d" % username_max_length, regex=r"^[\w.@+-]+$", error_messages={ "required" : "%s is required." % username_label, "max_length" : "%s is too long, maximum length is %d." % ( username_label, username_max_length ), "invalid": "%s may contain only letters, numbers and @/./+/-/_ characters." % username_label } )
    password1                   = forms.CharField( label="%s" % password1_label, max_length="%d" % password1_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password1_label, "max_length" : "%s is too long, maximum length is %d." % ( password1_label, password1_max_length ) })
    password2                   = forms.CharField( label="%s" % password2_label, max_length="%d" % password2_max_length, widget=forms.PasswordInput, error_messages={ "required" : "%s is required." % password2_label, "max_length" : "%s is too long, maximum length is %d." % ( password2_label, password2_max_length ) })
    email                       = forms.EmailField( label="%s" % email_label, max_length="%d" % email_max_length, error_messages={ "required" : "%s is required." % email_label, "max_length" : "%s is too long, maximum length is %d." % ( email_label, email_max_length ) } )

    class Meta( UserCreationForm.Meta ):
        fields                  = ( "first_name", "last_name", "username", "password1", "password2", "email" )
    

"""
User change (account details) form.

Author(s): Markku Laine
"""
class MyUserChangeForm( UserChangeForm ):
    first_name_label            = "First name"
    first_name_max_length       = 30
    last_name_label             = "Last name"
    last_name_max_length        = 30
    email_label                 = "E-mail address"
    email_max_length            = 128
    first_name                  = forms.CharField( label="%s" % first_name_label, max_length="%d" % first_name_max_length, error_messages={ "required" : "%s is required." % first_name_label, "max_length" : "%s is too long, maximum length is %d." % ( first_name_label, first_name_max_length ) } )
    last_name                   = forms.CharField( label="%s" % last_name_label, max_length="%d" % last_name_max_length, error_messages={ "required" : "%s is required." % last_name_label, "max_length" : "%s is too long, maximum length is %d." % ( last_name_label, last_name_max_length ) } )
    email                       = forms.EmailField( label="%s" % email_label, max_length="%d" % email_max_length, error_messages={ "required" : "%s is required." % email_label, "max_length" : "%s is too long, maximum length is %d." % ( email_label, email_max_length ) } )
    
    class Meta( UserChangeForm.Meta ):
        fields  = ( "username", "first_name", "last_name", "email" )
        
    def __init__( self, *args, **kwargs ):
        super( MyUserChangeForm, self ).__init__( *args, **kwargs )
        self.fields[ "username" ].widget.attrs[ "readonly" ]  = True
        #del self.fields[ "username" ] # This is a declared field we really want to be removed from the form to be rendered