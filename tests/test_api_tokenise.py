import json
from unittest import mock

import falcon
from hypothesis import given
from hypothesis import strategies as st

from paymentify.schemas import CardResourceRequest

# jsonschema regex
number_regex = CardResourceRequest['properties']['number']['pattern']
exp_month = CardResourceRequest['properties']['exp_month']['pattern']
exp_year = CardResourceRequest['properties']['exp_year']['pattern']
cvc = CardResourceRequest['properties']['cvc']['pattern']


def test_get_tokenise_not_allowed(client):
    response = client.simulate_get("/tokenise")

    assert response.status == falcon.HTTP_405


@given(
    st.from_regex(number_regex),
    st.from_regex(exp_month),
    st.from_regex(exp_year),
    st.from_regex(cvc),
)
def test_post_tokenise_valid_body(client, token, number, exp_month, exp_year, cvc):
    body = {
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
    }

    with mock.patch("stripe.Token.create") as mock_response:
        mock_response.return_value = token
        response = client.simulate_post("/tokenise", json=body)

    assert json.loads(response.content) == {
        "token_id": token.id,
        "created": token.created,
        "card": {
            "id": token.card.id,
            "exp_month": token.card.exp_month,
            "exp_year": token.card.exp_year,
            "last4": token.card.last4,
        },
    }
    assert response.status == falcon.HTTP_201


@given(st.text(), st.text(), st.text(), st.text())
def test_tokenise_post_invalid_payload(client, card_number, exp_month, exp_year, cvc):
    body = {
        "number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
    }

    with mock.patch("stripe.Token.create") as mock_response:
        response = client.simulate_post("/tokenise", json=body)

    mock_response.assert_not_called()
    assert response.status == falcon.HTTP_BAD_REQUEST
