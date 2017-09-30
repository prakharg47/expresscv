from __future__ import unicode_literals

from pyexpat import model

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Personal(models.Model):
    created_on = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=50, null=True)
    summary = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Education(models.Model):
    user = models.ForeignKey(User)

    college = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, default='M.Sc', null=True, blank=True)
    gpa = models.CharField(max_length=50, null=True, blank=True)

    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    from_year = models.CharField(max_length=50, default='2010', null=True, blank=True)
    to_year = models.CharField(max_length=50, default='2015', null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.college, self.major, self.gpa)


class Work(models.Model):

    user = models.ForeignKey(User)
    company = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    work_summary = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    from_year = models.CharField(max_length=50, default='2010')
    to_year = models.CharField(max_length=50, default='2010')

    def __str__(self):
        return "{}-{}".format(self.company, self.designation)