"""resumeroot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views as core_views
from app_core import views as app_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .settings import DEBUG

urlpatterns = [
    # Apps
    url(r'^auth/', include('authentication.urls')),
    url(r'^editor/', include('builder.urls')),
    url(r'^publish/', include('publish.urls')),
    url(r'^home/', app_views.home, name='home'),
    url(r'^$', app_views.home, name='root_home'),
    url(r'^blog', app_views.home, name='blog'),
    url(r'^pricing', app_views.pricing, name='pricing'),
    url(r'^upgrade', app_views.upgrade_user, name='upgrade'),
    url(r'^about', app_views.home, name='about'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^admin/', admin.site.urls),
]


if DEBUG:
   import debug_toolbar
   urlpatterns += [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ]

urlpatterns += staticfiles_urlpatterns()

