from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class BaseModel(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()

    class Meta:
        abstract = True


class Resume(TimeStampedModel):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    theme = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.name)


class Personal(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, max_length=200)
    mobile = models.CharField(max_length=200, null=True)
    linkedin_url = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    photo = models.FileField(upload_to="profile", null=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.email)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.resume:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Personal, self).save(*args, **kwargs)


class Summary(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True)
    # summary = models.CharField(max_length=2000, null=True)
    summary = models.TextField(null=True)


class Education(models.Model):
    resume = models.ForeignKey(Resume)

    college = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    gpa = models.CharField(max_length=200, null=True, blank=True)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    from_month = models.CharField(max_length=200, null=True, blank=True)
    from_year = models.CharField(max_length=200, null=True, blank=True)

    to_month = models.CharField(max_length=200, null=True, blank=True)
    to_year = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.college, self.major, self.gpa)


class Work(models.Model):

    resume = models.ForeignKey(Resume)
    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    from_year = models.CharField(max_length=200)
    to_year = models.CharField(max_length=200)

    work_summary = models.CharField(max_length=2000)

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


class Theme_Model(models.Model):
    THEMES_CHOICES = [
        ('standard', 'standard'),
        ('express', 'express'),
        ('compact', 'compact')
    ]

    FONTS = [
        ('computer modern', 'computer modern'),
        ('arial', 'arial'),
        ('calibri', 'calibri')
    ]

    resume = models.ForeignKey(Resume, primary_key=True, unique=True)
    theme = models.CharField(max_length=60, choices=THEMES_CHOICES, default='standard')

    font_size = models.DecimalField(max_digits=5, decimal_places=2)
    font_family = models.CharField(max_length=60, choices=FONTS, default='computer modern')
    horizontal_margins = models.DecimalField(max_digits=5, decimal_places=2)
    top_margin = models.DecimalField(max_digits=5, decimal_places=2)
    bottom_margin = models.DecimalField(max_digits=5, decimal_places=2)



