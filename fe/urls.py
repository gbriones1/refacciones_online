from django.conf.urls import patterns, include, url

from fe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add2cart/$', views.add2cart, name='add2cart'),
    url(r'^remove2cart/(?P<product_id>\w+)/$', views.remove2cart, name='remove2cart'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/logout/$', views.logout, name='logout'),
    url(r'^account/register/$', views.register, name='register'),
    url(r'^account/(?P<account_id>\w+)/$', views.view_account, name='view_account'),
    url(r'^product/$', views.product, name='product'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^order/$', views.order, name='order'),
    url(r'^order/(?P<product_id>\w+)/$', views.order_confirmation, name='order_confirmation'),
)
