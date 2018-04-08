from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views as custom_auth_views


urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', custom_auth_views.logout, name='logout'),
]
