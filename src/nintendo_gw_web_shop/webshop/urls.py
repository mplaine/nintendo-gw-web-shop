from django.conf.urls.defaults import *
from django.contrib.auth.views import password_reset, password_reset_done

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns    = patterns( '',
    ( r'^$', 'webshop.views.root' ),
    ( r'^home/$', 'webshop.views.home' ),
    ( r'^home/category/(?P<type_id>\d+)/', 'webshop.views.category' ),
    ( r'^home/search/', 'webshop.views.search' ),
    ( r'^register/$', 'webshop.views.register' ),
    ( r'^login/$', 'webshop.views.login' ),
#    ( r'^accounts/login/$', password_reset, { "template_name" : "registration/password_reset_form_markku.html" } ),
#    ( r'^accounts/resetdone/$', password_reset_done ),
    ( r'^login/forgotyourpassword/$', 'webshop.views.forgot_your_password' ),
#    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name' : 'registration/password_reset_email.html',  'post_reset_redirect': 'webshop.views.logout' }),
    ( r'^myaccount/$', 'webshop.views.myaccount' ),
    ( r'^myaccount/accountdetails/$', 'webshop.views.account_details' ),
    ( r'^myaccount/changepassword/$', 'webshop.views.change_password' ),
    ( r'^myaccount/addressbook/$', 'webshop.views.address_book' ),
    ( r'^myaccount/addressbook/new/$', 'webshop.views.address_book_new' ),
    ( r'^myaccount/addressbook/(?P<address_id>\d+)/edit/$', 'webshop.views.address_book_edit' ),
    ( r'^myaccount/addressbook/(?P<address_id>\d+)/delete/$', 'webshop.views.address_book_delete' ),
    ( r'^myaccount/completedorders/$', 'webshop.views.completed_orders' ),
    ( r'^logout/$', 'webshop.views.logout' ),
    ( r'^about/$', 'webshop.views.about' ),
    ( r'^credits/$', 'webshop.views.credits' ),
    ( r'^cart/$', 'webshop.views.cart' ),
    ( r'^payment/pay/$', 'webshop.views.payment_pay'),
    ( r'^payment/success/$', 'webshop.views.payment_success'),
    ( r'^payment/cancel/$', 'webshop.views.payment_cancel'),
    ( r'^payment/error/$', 'webshop.views.payment_error'),
    #ajax urls
    ( r'^ajax/product/(?P<product_id>\d+)/rating/$', 'webshop.views.rating'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #( r'^admin/', include( admin.site.urls ) ),
    ( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT } ),
)
