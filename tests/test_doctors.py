from .test_login_and_authorization import admin_login, data_string_into_dict

def test_post_doctors(client):
    admin_login(client)

    message = b'Success. Username is not registered yet.'
    doctor_datas = [
        {"name": "Doctor 2", "username": "doc2", "password": "pw2", "gender": "M", "birthdate": "2000-06-30", "work_start_time":"10:30:00", "work_end_time":"20:30:00"},
        {"name": "Doctor 3", "username": "doc3", "password": "pw3", "gender": "F", "birthdate": "2000-06-30", "work_start_time":"09:00:00", "work_end_time":"19:00:00"},
    ]
    for doctor_data in doctor_datas:
        post_response = client.post('/doctors', json=doctor_data)
        assert post_response.status_code == 200
        assert message in post_response.data


def test_post_registered_doctors(client):
    test_post_doctors(client)

    registered_doctor_data = {"name": "Doctor 2", "username": "doc2", "password": "pw2", "gender": "M", "birthdate": "2000-06-30", "work_start_time":"10:30:00", "work_end_time":"20:30:00"}
    post_response = client.post('/doctors', json=registered_doctor_data)
    message = b'Failed. Username has already been registered.'
    assert post_response.status_code == 200
    assert message in post_response.data


def test_get_doctors(client):
    test_post_doctors(client)

    get_all_response = client.get('/doctors')
    get_all_response_data = data_string_into_dict(get_all_response)
    assert len(get_all_response_data['doctors']) == 3 # plus Doctor 1
    assert get_all_response.status_code == 200


def test_get_an_doctor(client):
    test_post_doctors(client)

    doctor_usernames = ['doc1', 'doc2', 'doc3']
    for id, doctor_username in enumerate(doctor_usernames):
        get_response = client.get(f'/doctors/{id+1}')
        get_response_data = data_string_into_dict(get_response)['doctor']
        assert get_response_data['username'] == f'{doctor_username}'
        assert get_response.status_code == 200


def test_update_an_doctor(client):
    test_post_doctors(client)

    new_doctor2_data = {"name": "Updated Doctor 2", "username": "doc2_update", "password": "pw_new", "gender": "F", "birthdate": "2000-06-30", "work_start_time":"08:30:00", "work_end_time":"19:30:00"}
    update_response = client.put('/doctors/2', json=new_doctor2_data)
    assert update_response.status_code == 200

    get_response = client.get('/doctors/2')
    get_response_data = data_string_into_dict(get_response)['doctor']
    assert get_response_data['name'] == new_doctor2_data['name']
    assert get_response_data['username'] == new_doctor2_data['username']


def test_delete_an_doctor(client):
    test_post_doctors(client)

    delete_response = client.delete('/doctors/2')
    assert delete_response.status_code == 200

    get_all_response = client.get('/doctors')
    get_all_response_data = data_string_into_dict(get_all_response)['doctors']
    assert len(get_all_response_data) == 2
    doctor_names = [doctor_data['name'] for doctor_data in get_all_response_data]
    assert 'Doctor 1' in doctor_names
    assert 'Doctor 2' not in doctor_names
    assert 'Doctor 3' in doctor_names