from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
# Create your views here.
from .models import *


def home(request):

    total_users = len(User.objects.all())

    return render(request, 'app_core/home.html', context={'total_users': total_users})


def pricing(request):

    return render (request, 'app_core/pricing.html', {})

@login_required
def upgrade_user(request):
    """Ask user for payment and change status of user to PRO from BASIC"""

    # if payment is successful

    # if new user, create new subscription
    activation_date = datetime.datetime.now()
    expiry_date = datetime.datetime.today() + relativedelta(months=+3)
    user = request.user
    sub_type = 'PRO'

    new_sub = UserSubscription(user=user, valid_thru=expiry_date,
                               subscription_type=sub_type, created_on=activation_date)

    new_sub.save()
    return HttpResponseRedirect(reverse('home'))



