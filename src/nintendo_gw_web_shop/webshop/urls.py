from django.conf.urls.defaults import *

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
    ( r'^myaccount/$', 'webshop.views.myaccount' ),
    ( r'^myaccount/accountdetails/$', 'webshop.views.account_details' ),
    ( r'^myaccount/addressbook/$', 'webshop.views.address_book' ),
    ( r'^myaccount/completedorders/$', 'webshop.views.completed_orders' ),
    ( r'^logout/$', 'webshop.views.logout' ),
    ( r'^about/$', 'webshop.views.about' ),
    ( r'^credits/$', 'webshop.views.credits' ),
    ( r'^cart/$', 'webshop.views.cart' ),
    ( r'^payment/pay/$', 'webshop.views.payment_pay'),
    ( r'^payment/success/$', 'webshop.views.payment_success'),
    ( r'^payment/cancel/$', 'webshop.views.payment_cancel'),
    ( r'^payment/error/$', 'webshop.views.payment_error'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #( r'^admin/', include( admin.site.urls ) ),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT}),
)
