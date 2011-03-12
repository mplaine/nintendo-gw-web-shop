from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns    = patterns( '',
    ( r'^webshop/', include( 'webshop.urls' ) ),
    ( r'^admin/', include( admin.site.urls ) ),
)