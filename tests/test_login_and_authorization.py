endpoints = ['/employees', '/doctors', '/appointments', '/patients']


def data_string_into_dict(response):
    return eval(response.data.decode("utf-8").replace("null", "None"))

def admin_login(client):
    admin_data = {"username": "admin", "password": "pass"}
    login_response = client.post('/login', json=admin_data)
    login_message = b'Success. Username and password are registered.'
    assert login_message in login_response.data
    assert login_response.status_code == 200


def test_authorization(client, employee_active=False):
    for endpoint in endpoints:
        response = client.get(endpoint)
        message = b"There is no active employee at the moment."

        if employee_active:
            assert message not in response.data
            assert response.status_code == 200

        else:
            assert message in response.data
            assert response.status_code == 200


def test_authorization_after_doctor_login(client):
    doctor_data = {"username": "doc1", "password": "pw1"}
    
    login_response = client.post('/login', json=doctor_data)
    login_message = b'Success. Username and password are registered.'

    assert login_message in login_response.data
    assert login_response.status_code == 200

    test_authorization(client)


def test_authorization_after_employee_login(client):
    admin_login(client)
    test_authorization(client, employee_active=True)


def test_login_unregistered_user(client):
    false_user_data = {"username": "false_user", "password": "false_password"}
    response = client.post('/login', json=false_user_data)
    message = b'Failed. Username is not registered.'

    assert message in response.data
    assert response.status_code == 200


def test_login_false_password(client):
    false_password_data = {"username": "admin", "password": "false_password"}
    response = client.post('/login', json=false_password_data)
    message = b'Failed. Password does not match the username.'

    assert message in response.data
    assert response.status_code == 200
