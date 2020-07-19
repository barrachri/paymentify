import json
from unittest import mock

import pytest
import stripe
from hypothesis import given
from hypothesis import strategies as st

from paymentify.helpers import STRIPE_HTTP_STATUS_ERROR, stripe_catcher


@pytest.mark.parametrize("http_status", STRIPE_HTTP_STATUS_ERROR.keys())
def test_stripe_catcher(http_status):
    err_message = "This is an error from stripe"
    err_type = "processor_error"

    @stripe_catcher
    def raise_stripe_error():
        raise stripe.error.StripeError(
            json_body={"error": {"message": err_message, "type": err_type}},
            http_status=http_status,
        )

    response, status = raise_stripe_error()

    assert response == {
        'message': err_message,
        'type': err_type,
    }
    assert status == STRIPE_HTTP_STATUS_ERROR[http_status]


@given(
    st.text(min_size=5), st.integers(min_value=1),
)
def test_stripe_catcher_e2e(client, token, amount):
    err_message = "This is an error from stripe"
    err_type = "processor_error"
    http_status = 403
    body = {
        "token": token,
        "amount": amount,
    }

    with mock.patch("stripe.Charge.create") as mock_response:
        err = stripe.error.StripeError(
            json_body={"error": {"message": err_message, "type": err_type}},
            http_status=http_status,
        )
        mock_response.side_effect = err
        response = client.simulate_post("/sale", json=body)

    mock_response.assert_called_with(source=token, amount=amount)
    assert json.loads(response.content) == {
        'message': err_message,
        'type': err_type,
    }
    assert response.status == STRIPE_HTTP_STATUS_ERROR[http_status]
