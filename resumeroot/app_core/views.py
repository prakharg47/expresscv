from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
# Create your views here.
from paypal.standard.forms import PayPalPaymentsForm

from .models import *


def home(request):

    total_users = len(User.objects.all())

    return render(request, 'app_core/home.html', context={'total_users': total_users})


def pricing(request):
    # What you want the button to do.
    import datetime

    print ("""
        HELLOOOO
    """)

    print(request.user.id)
    print("^^^^^^^^^^^^^^^ ID")

    paypal_dict = {
        "business": "prakhar11509@gmail.com",
        "amount": "1.00",
        "item_name": "pro subscription",
        "invoice": str(datetime.datetime.now()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('upgrade')),
        "cancel_return": request.build_absolute_uri(reverse('pricing')),
        "custom" : str(request.user.id)
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render (request, 'app_core/pricing.html', {'form': form})

@login_required
def upgrade_user(request):
    """Ask user for payment and change status of user to PRO from BASIC"""

    # if payment is successful

    # if new user, create new subscription
    activation_date = datetime.datetime.now()
    expiry_date = datetime.datetime.today() + relativedelta(months=+3)
    user = request.user
    user1 = User()


    sub_type = 'PRO'

    new_sub = UserSubscription(user=user, valid_thru=expiry_date,
                               subscription_type=sub_type, created_on=activation_date)

    new_sub.save()
    return HttpResponseRedirect(reverse('home'))


def payment_done(request):
    return render(request, 'app_core/payment_done.html', {})