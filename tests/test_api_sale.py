import falcon


def test_get_sale_not_allowed(client):
    response = client.simulate_get("/sale")

    assert response.status == falcon.HTTP_405
