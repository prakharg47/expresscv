from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^(?P<resume_id>[0-9]+)/personal$', views.personal, name='personal'),
    url(r'^(?P<resume_id>[0-9]+)/summary$', views.summary, name='summary'),

    url(r'^(?P<resume_id>[0-9]+)/education$', views.education_all, name='education'),
    url(r'^(?P<resume_id>[0-9]+)/education/edit$', views.education_new, name='education_new'),
    url(r'^(?P<resume_id>[0-9]+)/education/edit/(?P<ed_id>[0-9]+)$$', views.education_edit, name='education_edit'),
    url(r'^(?P<resume_id>[0-9]+)/education/delete/(?P<ed_id>[0-9]+)$$', views.education_delete, name='education_delete'),

    url(r'^(?P<resume_id>[0-9]+)/experience$', views.experience_all, name='experience'),
    url(r'^(?P<resume_id>[0-9]+)/experience/edit$', views.experience_new, name='experience_new'),
    url(r'^(?P<resume_id>[0-9]+)/experience/edit/(?P<work_id>[0-9]+)$', views.experience_edit, name='experience_edit'),
    url(r'^(?P<resume_id>[0-9]+)/experience/delete/(?P<work_id>[0-9]+)$', views.experience_delete, name='experience_delete'),

    url(r'^(?P<resume_id>[0-9]+)/skills$', views.skills, name='skills'),
    url(r'^(?P<resume_id>[0-9]+)/languages$', views.languages, name='languages'),

    url(r'^(?P<resume_id>[0-9]+)/awards$', views.award_all, name='award'),
    url(r'^(?P<resume_id>[0-9]+)/awards/edit$', views.award_new, name='award_new'),
    url(r'^(?P<resume_id>[0-9]+)/awards/edit/(?P<award_id>[0-9]+)$', views.award_edit, name='award_edit'),
    url(r'^(?P<resume_id>[0-9]+)/awards/delete/(?P<award_id>[0-9]+)$', views.award_delete, name='award_delete'),

    # name changed to avoid any django clashing
    url(r'^(?P<resume_id>[0-9]+)/theme', views.theme, name='theme'),

    url(r'^resume$', views.resume, name='resume'),
    url(r'^resume/(?P<resume_id>[0-9]+)/delete$', views.delete_resume, name='delete_resume'),

    # url(r'^(?P<resume_id>[0-9]+)/publish$', views.publish, name='publish'),
    # url(r'^(?P<resume_id>[0-9]+)/preview', views.preview, name='preview'),
]
