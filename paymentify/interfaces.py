from typing import Mapping, Tuple

import falcon
import stripe

from paymentify.helpers import stripe_catcher
from paymentify.models import Card, Charge

# Types
Response = Tuple[Mapping, str]


@stripe_catcher
def create_token(card: Card) -> Response:
    token = stripe.Token.create(
        card={
            "number": card.number,
            "exp_month": card.exp_month,
            "exp_year": card.exp_year,
            "cvc": card.cvc,
        },
    )
    return (
        {
            "token_id": token.id,
            "created": token.created,
            "card": {
                "id": token.card.id,
                "exp_month": token.card.exp_month,
                "exp_year": token.card.exp_year,
                "last4": token.card.last4,
            },
        },
        falcon.falcon.HTTP_201,
    )


@stripe_catcher
def create_charge(charge: Charge) -> Response:
    charge = stripe.Charge.create(amount=charge.amount, source=charge.token)
    return (
        {
            "id": charge.id,
            "amount": charge.amount,
            "payment_method": charge.payment_method,
            "paid": charge.paid,
            "status": charge.status,
            "created": charge.created,
        },
        falcon.falcon.HTTP_201,
    )
