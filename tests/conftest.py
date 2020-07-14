import pytest
from falcon import testing

from paymentify.main import api


@pytest.fixture
def client():
    return testing.TestClient(api)
