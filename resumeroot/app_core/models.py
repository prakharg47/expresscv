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


class UserProfile(models.Model):
    """
    plans :

    0 - basic
    1 - pro

    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    plan = models.IntegerField(max_length=50, default=0,null=False, blank=False)
    expiry_date = models.DateTimeField()
    job_suggestions = models.BooleanField(default=True)
    referral_code = models.CharField(max_length=50)
    referred_by = models.ForeignKey(User)






from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

# from .models import UserProfile

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "receiver_email@example.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        print ("IPN OBJECT - {}".format(str(ipn_obj)))

        # profile = UserProfile(user=)
        # pro
        # profile.save()

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "premium_plan":
            price = 10
        else:
            price = 1000

        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
            pass

        print("price is {}".format(str(price)))
    else:
        #...
        print("Do nothing ....")

valid_ipn_received.connect(show_me_the_money)

