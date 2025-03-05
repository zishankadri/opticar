from paypal.standard.ipn.signals import valid_ipn_received
from project.core.hooks import show_me_the_money


class MockIPN:
    receiver_email = 'sb-dvlc126188630@business.example.com'
    mc_currency = 'USD'
    custom = 1  # example user ID from your system
    item_name = 92  # example booking ID from your system
    payment_status = 'Completed'

# Create a mock IPN object
mock_ipn = MockIPN()

valid_ipn_received.send(sender=mock_ipn)
