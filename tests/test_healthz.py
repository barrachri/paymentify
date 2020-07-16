import falcon


def test_healthz(client):
    response = client.simulate_get("/healthz")

    assert response.status == falcon.HTTP_200
