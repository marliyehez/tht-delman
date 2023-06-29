from .test_login_and_authorization import admin_login, data_string_into_dict

def test_post_employees(client):
    admin_login(client)

    message = b'Success. Username is not registered yet.'
    employee_datas = [
        {"name": "Employee 1", "username": "emp1", "gender": "M", "password": "pass1", "birthdate": "2023-06-30" },
        {"name": "Employee 2", "username": "emp2", "gender": "F", "password": "pass2", "birthdate": "2023-06-30" },
    ]
    for employee_data in employee_datas:
        post_response = client.post('/employees', json=employee_data)
        assert post_response.status_code == 200
        assert message in post_response.data

def test_post_registered_employees(client):
    test_post_employees(client)

    registered_employee_data = {"name": "Employee 2", "username": "emp2", "gender": "F", "password": "pass2", "birthdate": "2023-06-30" }
    post_response = client.post('/employees', json=registered_employee_data)
    message = b'Failed. Username has already been registered.'
    assert post_response.status_code == 200
    assert message in post_response.data


def test_get_employees(client):
    test_post_employees(client)

    get_all_response = client.get('/employees')
    get_all_response_data = data_string_into_dict(get_all_response)
    assert len(get_all_response_data['employees']) == 3 # plus admin
    assert get_all_response.status_code == 200


def test_get_an_employee(client):
    test_post_employees(client)

    employee_usernames = ['admin', 'emp1', 'emp2']
    for id, employee_username in enumerate(employee_usernames):
        get_response = client.get(f'/employees/{id+1}')
        get_response_data = data_string_into_dict(get_response)['employee']
        assert get_response_data['username'] == f'{employee_username}'
        assert get_response.status_code == 200


def test_update_an_employee(client):
    test_post_employees(client)

    new_employee3_data = {"name": "Updated Employee 2", "username": "emp2_update", "gender": "M", "password": "pass_new", "birthdate": "2023-06-30" }
    update_response = client.put('/employees/3', json=new_employee3_data)
    assert update_response.status_code == 200

    get_response = client.get('/employees/3')
    get_response_data = data_string_into_dict(get_response)['employee']
    assert get_response_data['name'] == new_employee3_data['name']
    assert get_response_data['username'] == new_employee3_data['username']


def test_delete_an_employee(client):
    test_post_employees(client)

    delete_response = client.delete('/employees/2')
    assert delete_response.status_code == 200

    get_all_response = client.get('/employees')
    get_all_response_data = data_string_into_dict(get_all_response)['employees']
    assert len(get_all_response_data) == 2
    employee_names = [employee_data['name'] for employee_data in get_all_response_data]
    assert 'Admin' in employee_names
    assert 'Employee 1' not in employee_names
    assert 'Employee 2' in employee_names