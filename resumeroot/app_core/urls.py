from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.home, name='home'),
    url(r'^home', views.home, name='home'),
    url(r'^upgrade', views.upgrade_user, name='upgrade')
]
