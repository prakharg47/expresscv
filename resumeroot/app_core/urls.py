from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='root_home'),
    url(r'^home', views.home, name='home'),
    url(r'^upgrade', views.upgrade_user, name='upgrade'),
    url(r'^done', views.payment_done, name='payment_done'),

    url(r'^blog', views.home, name='blog'),
    url(r'^pricing', views.pricing, name='pricing'),

    url(r'^about', views.home, name='about'),
    url(r'^account', views.account, name='accoun'),

]
