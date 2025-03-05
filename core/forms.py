from django import forms
from django.utils.safestring import mark_safe

from .models import Car


class CarFilterForm(forms.Form):
    seats = forms.MultipleChoiceField(
        choices= Car.SEATS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    make_and_model = forms.MultipleChoiceField(
        choices=Car.MAKE_AND_MODEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    car_type = forms.MultipleChoiceField(
        choices=Car.CAR_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html


class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    # def get_html_submit_element(self):
        # return """<button type="btn-primary"> Continue With PayPal </button>"""
    
    def render(self, *args, **kwargs):
        if not args and not kwargs:
            # `form.render` usage from template
            return format_html(
        
            """<form id="paypal-form" action="{0}" method="post">
                {1}
                <button type="submit" class="btn-primary" id="paypal-button"> Continue on Paypal </button>
    
                </form>""",
    
            self.get_login_url(),
            self.as_p(),
            self.get_image(),
        )
        else:
            # Need to delegate to super. This provides
            # support for `as_p` method and for `BoundField.label_tag`,
            # and perhaps others.
            return super().render(*args, **kwargs)