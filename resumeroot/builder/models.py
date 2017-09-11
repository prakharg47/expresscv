from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class ResumeConfig(models.Model):

    created_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.IntegerField()

    def __str__(self):
        return self.name


class Education(models.Model):

    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    gpa = models.CharField(max_length=50)
    resume = models.ForeignKey(ResumeConfig)



