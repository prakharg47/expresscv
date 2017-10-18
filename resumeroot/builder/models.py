from __future__ import unicode_literals

from pyexpat import model

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()

    class Meta:
        abstract = True


class Resume(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class Personal(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=200, null=True)
    # summary = models.CharField(max_length=2000, null=True)
    linkedin_url = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    photo = models.FileField(upload_to="profile", null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.resume:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Personal, self).save(*args, **kwargs)


class Summary(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True)
    summary = models.CharField(max_length=2000, null=True)


class Education(models.Model):
    resume = models.ForeignKey(Resume)

    college = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    gpa = models.CharField(max_length=200, null=True, blank=True)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    from_year = models.CharField(max_length=200, null=True, blank=True)
    to_year = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.college, self.major, self.gpa)


class Work(models.Model):

    resume = models.ForeignKey(Resume)
    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    work_summary = models.CharField(max_length=2000)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    from_year = models.CharField(max_length=200)
    to_year = models.CharField(max_length=200)

    def __str__(self):
        return "{}-{}".format(self.company, self.designation)


class Skills(models.Model):

    resume = models.ForeignKey(Resume, primary_key=True)
    technical = models.CharField(max_length=300)
    management = models.CharField(max_length=300)

    def __str__(self):
        return "{}".format(self.technical)


class Languages(models.Model):

    resume = models.ForeignKey(Resume, primary_key=True)
    languages = models.CharField(max_length=300)


