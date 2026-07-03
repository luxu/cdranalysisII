def test_home_status(client):
    response = client.get('/')
    assert response.status_code == int(302)
