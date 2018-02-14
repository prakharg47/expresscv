from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^(?P<resume_id>[0-9]+)/personal$', views.personal, name='personal'),
    url(r'^(?P<resume_id>[0-9]+)/summary$', views.summary, name='summary'),
    url(r'^(?P<resume_id>[0-9]+)/education$', views.education, name='education'),
    url(r'^(?P<resume_id>[0-9]+)/experience$', views.experience, name='experience'),
    url(r'^(?P<resume_id>[0-9]+)/experience2$', views.experience2, name='experience2'),
    url(r'^(?P<resume_id>[0-9]+)/skills$', views.skills, name='skills'),
    url(r'^(?P<resume_id>[0-9]+)/languages$', views.languages, name='languages'),

    # name changed to avoid any django clashing
    url(r'^(?P<resume_id>[0-9]+)/theme', views.theme, name='theme'),

    url(r'^resume$', views.resume, name='resume'),
    url(r'^resume/(?P<resume_id>[0-9]+)/delete$', views.delete_resume, name='delete_resume'),

    url(r'^(?P<resume_id>[0-9]+)/publish$', views.publish, name='publish'),
    url(r'^(?P<resume_id>[0-9]+)/preview', views.preview, name='preview'),
]
