from django.conf.urls.defaults import patterns
from django.contrib import admin

import settings
admin.autodiscover()


urlpatterns    = patterns( '',
    ( r'^$', 'webshop.views.root' ),
    ( r'^home/$', 'webshop.views.home' ),
    ( r'^home/category/(?P<type_id>\d+)/', 'webshop.views.category' ),
    ( r'^home/search$', 'webshop.views.search' ),
    ( r'^register/$', 'webshop.views.register' ),
    ( r'^login/$', 'webshop.views.login' ),
    ( r'^passwordreset/$', 'webshop.views.password_reset' ),
    ( r'^passwordreset/requestnewpassword/$', 'webshop.views.request_new_password' ), # Request new password
    ( r'^passwordreset/newpasswordrequested/$', 'webshop.views.new_password_requested' ), # New password requested
    ( r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name' : 'webshop/passwordreset/new_password.html',  'post_reset_redirect': '/webshop/passwordreset/newpasswordset/' } ), # New Password
    ( r'^passwordreset/newpasswordset/$', 'webshop.views.new_password_set' ), # New password set
    ( r'^logout/$', 'webshop.views.logout' ),
    ( r'^myaccount/$', 'webshop.views.myaccount' ),
    ( r'^myaccount/accountdetails/$', 'webshop.views.account_details' ),
    ( r'^myaccount/changepassword/$', 'webshop.views.change_password' ),
    ( r'^myaccount/addressbook/$', 'webshop.views.address_book' ),
    ( r'^myaccount/addressbook/new/$', 'webshop.views.address_book_new' ),
    ( r'^myaccount/addressbook/(?P<address_id>\d+)/edit/$', 'webshop.views.address_book_edit' ),
    ( r'^myaccount/addressbook/(?P<address_id>\d+)/delete/$', 'webshop.views.address_book_delete' ),
    ( r'^myaccount/completedorders/$', 'webshop.views.completed_orders' ),
    ( r'^admin/$', 'webshop.views.admin' ),
    ( r'^admin/paidorders/$', 'webshop.views.admin_paid_orders' ),
    ( r'^admin/deliveredorders/$', 'webshop.views.admin_delivered_orders' ),
    ( r'^admin/statistics/$', 'webshop.views.admin_statistics' ),
    ( r'^about/$', 'webshop.views.about' ),
    ( r'^credits/$', 'webshop.views.credits' ),
    ( r'^cart/$', 'webshop.views.cart' ),
    ( r'^cart/add$', 'webshop.views.add_to_cart' ),
    ( r'^cart/update$', 'webshop.views.update_cart' ),  
    ( r'^cart/empty/$', 'webshop.views.empty_cart' ),
    ( r'^payment/pay/$', 'webshop.views.payment_pay'),
    ( r'^payment/confirm$', 'webshop.views.payment_confirm'),
    ( r'^payment/success$', 'webshop.views.payment_success'),
    ( r'^payment/cancel$', 'webshop.views.payment_cancel'),
    ( r'^payment/error$', 'webshop.views.payment_error'),
    
    #Ajax urls
    ( r'^ajax/product/(?P<product_id>\d+)/rating/$', 'webshop.views.rating'),
    ( r'^ajax/product/(?P<product_id>\d+)/comment/$', 'webshop.views.comment'),
    ( r'^ajax/products/$', 'webshop.views.ajaxproducts'),
    ( r'^ajax/statistics/commentcount/$', 'webshop.views.ajaxstatisticscommentcount'),
    ( r'^ajax/product/(?P<product_id>\d+)/view/$', 'webshop.views.addproductview'),
    ( r'^ajax/product/view/$', 'webshop.views.productview'),
    ( r'^ajax/comment/(?P<comment_id>\d+)/delete/$', 'webshop.views.commentdelete'),

    # Static files
    ( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT } ),
)