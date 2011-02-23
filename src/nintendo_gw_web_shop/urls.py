from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns    = patterns( '',
    ( r'^polls/', include( 'polls.urls' ) ),
    ( r'^webshop/', include( 'webshop.urls' )),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    ( r'^admin/', include( admin.site.urls ) ),
)