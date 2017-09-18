from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.home, name='builder_home'),
    url(r'^personal$', views.personal, name='personal'),
    url(r'^education$', views.education, name='education'),
    url(r'^experience$', views.experience, name='experience' ),
    url(r'^publish$', views.publish, name='publish')
]
