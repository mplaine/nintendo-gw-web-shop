from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns    = patterns( '',
    ( r'^$', 'webshop.views.home'),
    ( r'^home/$', 'webshop.views.home'),
    ( r'^home/category/', 'webshop.views.category'),
    ( r'^home/search/', 'webshop.views.search'),
    ( r'^register/', 'webshop.views.register'),
    ( r'^add/', 'webshop.views.add_product'),
    ( r'^products/', 'webshop.views.view_products'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #( r'^admin/', include( admin.site.urls ) ),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT}),
)