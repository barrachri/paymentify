import pytest
from falcon import testing

from paymentify.main import api


@pytest.fixture(scope="module")
def client():
    return testing.TestClient(api)


@pytest.fixture(scope="module")
def token():
    class MockedToken:
        id = "tok_1H5VCmLc6lT5RCtGLvo2LSmC"
        created = 1594898688

        class card:
            id = "card_1H5VCmLc6lT5RCtGSWahXZPJ"
            exp_month = 7
            exp_year = 21
            last4 = 4242

    return MockedToken


@pytest.fixture(scope="module")
def charge():
    class MockedCharge:
        id = "ch_1H6HA0Lc6lT5RCtGK5QMjc8S"
        amount = 2000
        payment_method = "card_1H6C5eLc6lT5RCtGc9WIqjc5"
        paid = True
        status = "succeeded"
        created = 1594898688

    return MockedCharge
