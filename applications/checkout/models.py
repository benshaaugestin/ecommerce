from django.db import models
from ecom import settings

class Tokens(models.Model):
    """
        Stripe token generator
    """
    charge_id = models.CharField(max_length=32,blank=True)

    def __init__(self, *args, **kwargs):
        super(Tokens, self).__init__(*args, **kwargs)

        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

    def charge(self, price_in_cents, email, number, exp_month, exp_year, cvc, token):
        if self.charge_id:
            return False, Exception(message="Already charged.")
        try:
            response = self.stripe.Charge.create(
                currency="usd",
                source=token,
                description='Payment Successfull!')

            self.charge_id = response.id
        except self.stripe.CardError:
            return False, {'message': 'Failed'}

        return True, response
