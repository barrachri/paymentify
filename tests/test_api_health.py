import falcon


def test_health(client):
    response = client.simulate_get("/health")

    assert response.status == falcon.HTTP_200
