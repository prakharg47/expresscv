from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.home, name='builder_home'),
    url(r'^(?P<resume_id>[0-9]+)/personal$', views.personal, name='personal'),
    url(r'^(?P<resume_id>[0-9]+)/education$', views.education, name='education'),
    url(r'^(?P<resume_id>[0-9]+)/experience$', views.experience, name='experience'),
    url(r'^(?P<resume_id>[0-9]+)/skills$', views.skills, name='skills'),

    url(r'^resume$', views.resume, name='resume'),
    url(r'^resume/(?P<resume_id>[0-9]+)/delete$', views.delete_resume, name='delete_resume'),

    url(r'^(?P<resume_id>[0-9]+)/publish$', views.publish, name='publish')
]
