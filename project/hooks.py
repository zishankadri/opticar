# paypal_hooks.py
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone

from django.shortcuts import get_object_or_404
from accounts.models import UserAccount
from django.dispatch import receiver
from accounts.utils import send_email


# @receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL: 
        return # Invalid payment
    if ipn_obj.mc_currency != 'USD': return # Invalid payment
    
    user = UserAccount.objects.get(id=ipn_obj.custom)

    if not valid_creation(ipn_obj, user):
        user.subscription_status = "INVALID"
        user.save()
        # return
        # Successful Transaction give the users what they want.
        user.is_paid_member = True
        user.subscription_status = "ACTIVE"
        
        # user.subsciption_period = ipn_obj.period3 # "1 M" or "1 Y"
        
        user.save()
        # Send Thank You email to user
        subject = f"Access Granted to {settings.SITE_NAME} Subscription!"
        message = f'''
        We are delighted to inform you that your payment for the {settings.SITE_NAME} subscription has been successfully processed. Your account is now active, and you can start using our service immediately.
        
        {settings.DEFAUL_DOMAIN}/classes/
        '''
        send_email(subject=subject, message=message, email=user.email)
        
    if not ipn_obj.payment_status == ST_PP_COMPLETED:
        # return
        user.is_paid_member = True
        user.save
        # user.last_payment_date = timezone.localdate()
    

valid_ipn_received.connect(show_me_the_money)
    

def valid_creation(ipn_obj, user):
    if ipn_obj.recurring != "1": return False
    
    if ipn_obj.period3 == "1 M":
    # Trial period duration check
        if ipn_obj.period1 != "1 M":
            return False

    # Trial period price check
    if ipn_obj.amount1 != settings.MONTHLY_PRICE:
        return False

    # Regular subscription price check
    
    if ipn_obj.amount3 != settings.MONTHLY_PRICE:
        return False
    elif ipn_obj.period3 == "1 Y":
        # Trial period duration check
        if ipn_obj.period1 != "1 Y":
            return False
        # Trial period price check
        if ipn_obj.amount1 != settings.YEARLY_PRICE:
            return False
        # Regular subscription price check
        if ipn_obj.amount3 != settings.YEARLY_PRICE:
            return False
            
        return True
    
valid_ipn_received.connect(show_me_the_money)


# def valid_transaction(ipn_obj, user):
#     user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)
    
#     if not ipn_obj.payment_status == ST_PP_COMPLETED:
#         return False
#     if user.subscription_status == "INVALID":
#         return False
        
#     return True