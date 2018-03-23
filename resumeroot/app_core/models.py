from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserSubscription(models.Model):
    user = models.ForeignKey(User)

    valid_thru = models.DateTimeField() # expiry date
    subscription_type = models.CharField(max_length=50, null=False)
    is_expired = models.BooleanField(default=False)
    created_on = models.DateTimeField() # activation date
