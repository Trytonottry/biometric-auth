def test_login_api(client):
    response = client.post('/api/login', json={
        "username": "testuser",
        "methods": ["face"],
        "liveness_verified": True
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'token' in json_data
    assert json_data['success'] is True

def test_register_api(client):
    response = client.post('/api/register', json={
        "username": "newuser",
        "role": "user",
        "access_level": 1,
        "enable_face": True
    })
    assert response.status_code == 201
    assert response.get_json()['success'] is True