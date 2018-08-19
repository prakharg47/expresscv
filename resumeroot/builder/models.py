from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager


class Resume(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return "{}".format(self.name)

class Theme(models.Model):

    THEME_NAMES = ['Specter', 'Ross', 'Donna', 'Louie']
    THEME_CHOICES = [(e,e) for e in THEME_NAMES]
    FONT_NAMES = ['Computer Modern', 'Sans', 'Teletype']
    FONT_CHOICES = [(e,e) for e in FONT_NAMES]

    resume = models.ForeignKey(Resume, primary_key=True, unique=True, on_delete=models.CASCADE)

    theme = models.CharField(max_length=60, choices=THEME_CHOICES, default='1')
    font_size = models.IntegerField(default=11)
    font_family = models.CharField(max_length=60, choices=FONT_CHOICES, default='Sans')
    horizontal_margins = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    top_margin = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    bottom_margin = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)


class Personal(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, max_length=200)
    mobile = models.CharField(max_length=200, null=True)
    title = models.CharField(null=True, max_length=200, blank=True)
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
    resume = models.ForeignKey(Resume, primary_key=True, on_delete=models.CASCADE)
    summary = models.TextField(null=True)


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    college = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    gpa = models.CharField(max_length=200, null=True, blank=True)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    from_year = models.CharField(max_length=200, null=True, blank=True)
    to_year = models.CharField(max_length=200, null=True, blank=True)

    education_summary = models.TextField(null=True)

    def __str__(self):
        return "{}, {}, {}".format(self.college, self.major, self.degree)


class Work(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    from_year = models.CharField(max_length=200)
    to_year = models.CharField(max_length=200)
    work_summary = models.CharField(max_length=2000)

    def __str__(self):
        return "{}-{}".format(self.company, self.designation)

class Award(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    award_name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    award_summary = models.CharField(max_length=2000)

    def __str__(self):
        return "{}, {}".format(self.award_name, self.organisation)


class Skills(models.Model):

    resume = models.ForeignKey(Resume, primary_key=True, on_delete=models.CASCADE)
    skills = models.TextField(null=True)
    # technical = models.CharField(max_length=300)
    # management = models.CharField(max_length=300)

    def __str__(self):
        return "{}".format(self.skills[0:50])


class Languages(models.Model):
    resume = models.ForeignKey(Resume, primary_key=True, on_delete=models.CASCADE)
    languages = models.TextField(null=True)





