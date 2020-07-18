import json
from unittest import mock

import falcon
from hypothesis import given
from hypothesis import strategies as st


def test_get_sale_not_allowed(client):
    response = client.simulate_get("/sale")

    assert response.status == falcon.HTTP_405


@given(
    st.text(min_size=5), st.integers(min_value=1),
)
def test_post_sale_valid_body(client, charge, token, amount):
    body = {
        "token": token,
        "amount": amount,
    }

    with mock.patch("stripe.Charge.create") as mock_response:
        mock_response.return_value = charge
        response = client.simulate_post("/sale", json=body)

    assert json.loads(response.content) == {
        "id": charge.id,
        "amount": charge.amount,
        "payment_method": charge.payment_method,
        "paid": charge.paid,
        "status": charge.status,
        "created": charge.created,
    }
    assert response.status == falcon.HTTP_201


@given(st.text(max_size=4), st.floats())
def test_post_sale_invalid_body(client, charge, token, amount):
    body = {
        "token": token,
        "amount": amount,
    }

    with mock.patch("stripe.Charge.create") as mock_response:
        response = client.simulate_post("/sale", json=body)

    mock_response.assert_not_called()
    assert response.status == falcon.HTTP_BAD_REQUEST
