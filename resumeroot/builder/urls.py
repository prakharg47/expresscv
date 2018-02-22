from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^(?P<resume_id>[0-9]+)/personal$', views.personal, name='personal'),
    url(r'^(?P<resume_id>[0-9]+)/summary$', views.summary, name='summary'),
    url(r'^(?P<resume_id>[0-9]+)/education$', views.education, name='education'),

    url(r'^(?P<resume_id>[0-9]+)/experience$', views.experience_all, name='experience'),
    url(r'^(?P<resume_id>[0-9]+)/experience/edit$', views.experience_new, name='experience_new'),
    url(r'^(?P<resume_id>[0-9]+)/experience/edit/(?P<work_id>[0-9]+)$', views.experience_edit, name='experience_edit'),
    url(r'^(?P<resume_id>[0-9]+)/experience/delete/(?P<work_id>[0-9]+)$', views.experience_delete, name='experience_delete'),

    url(r'^(?P<resume_id>[0-9]+)/skills$', views.skills, name='skills'),
    url(r'^(?P<resume_id>[0-9]+)/languages$', views.languages, name='languages'),

    # name changed to avoid any django clashing
    url(r'^(?P<resume_id>[0-9]+)/theme', views.theme, name='theme'),

    url(r'^resume$', views.resume, name='resume'),
    url(r'^resume/(?P<resume_id>[0-9]+)/delete$', views.delete_resume, name='delete_resume'),

    url(r'^(?P<resume_id>[0-9]+)/publish$', views.publish, name='publish'),
    url(r'^(?P<resume_id>[0-9]+)/preview', views.preview, name='preview'),
]
