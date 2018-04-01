import datetime

from dateutil.relativedelta import relativedelta
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import UserProfile

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "prakhar11509@gmail.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        print(""" XXXXXXXXXXXX""")
        print(ipn_obj.custom)

        profile = UserProfile(user_id=ipn_obj.custom)
        profile.expiry_date = datetime.datetime.today() + relativedelta(months=+3)
        profile.plan = 1
        profile.save()

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

