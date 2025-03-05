# paypal_hooks.py
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone

from accounts.models import UserAccount
from django.dispatch import receiver
from accounts.utils import send_email

from core.models import Booking

import logging
logger = logging.getLogger('django')

# @receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    logger.warning(f"ipn_obj Received : {ipn_obj}")

    
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        return # Invalid payment
    if ipn_obj.mc_currency != 'USD': return # Invalid payment
    
    user = UserAccount.objects.get(id=ipn_obj.custom)

    booking = Booking.objects.get(id=ipn_obj.item_name)
    booking.status = Booking.IN_PROGRESS
    booking.payment_method = Booking.ONLINE

    booking.save()

    if not ipn_obj.payment_status == ST_PP_COMPLETED:
        pass

valid_ipn_received.connect(show_me_the_money)


def valid_transaction(ipn_obj, user):
    user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)
    
    if not ipn_obj.payment_status == ST_PP_COMPLETED:
        return False
    if user.subscription_status == "INVALID":
        return False
        
    return True