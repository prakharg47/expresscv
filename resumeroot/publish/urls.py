from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    url(r'^(?P<resume_id>[0-9]+)/publish$', views.publish, name='publish'),
    url(r'^(?P<resume_id>[0-9]+)/preview', views.preview, name='preview'),
]
