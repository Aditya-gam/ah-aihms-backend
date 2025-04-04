def test_status_route_success(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/status' endpoint is requested (GET)
    THEN check that the response is valid and the status message is returned
    """
    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json == {"status": "auth route working"}


def test_status_route_invalid_method(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a non-GET method (e.g., POST) is sent to '/api/auth/status'
    THEN check that the endpoint returns a 405 METHOD NOT ALLOWED
    """
    response = client.post("/api/auth/status")
    assert response.status_code == 405
