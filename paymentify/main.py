import os

import falcon
import stripe
from dynaconf import settings
from falcon.media.validators import jsonschema

from paymentify import models as m
from paymentify import schemas as s
from paymentify.interfaces import create_charge, create_token


class HealthcheckResource:
    def on_get(self, req, resp):
        """Health check endpoint"""
        resp.media = {"version": os.environ.get("GIT_HASH", None)}
        resp.status = falcon.HTTP_200


class CardResource:
    @jsonschema.validate(s.CardResourceRequest)
    def on_post(self, req, resp):
        """Handles Token creation"""

        card = m.Card(**req.media)

        resp.media, resp.status = create_token(card)


class SaleResource:
    @jsonschema.validate(s.SaleResourceSchema)
    def on_post(self, req, resp):
        """Handles Sale (charge) creation"""

        charge = m.Charge(**req.media)

        resp.media, resp.status = create_charge(charge)


class Api(falcon.API):
    def __init__(self):
        super().__init__()

        # Set up STRIPE API key
        stripe.api_key = settings.get("STRIPE_API_KEY", "SET-YOUR-KEY")


api = Api()
api.add_route("/health", HealthcheckResource())
api.add_route("/tokenise", CardResource())
api.add_route("/sale", SaleResource())
