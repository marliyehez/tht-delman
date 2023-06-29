from .test_login_and_authorization import admin_login, data_string_into_dict

def test_post_patients(client):
    admin_login(client)

    message = b'Success. ID card number is not registered yet.'
    patient_datas = [
        {"name": "Patient 1", "gender": "M", "birthdate": "1991-01-01", "no_ktp": 9991, "address": 'address1'},
        {"name": "Patient 2", "gender": "F", "birthdate": "1992-02-02", "no_ktp": 9992, "address": 'address2'},
        {"name": "Patient 3", "gender": "M", "birthdate": "1993-03-03", "no_ktp": 9993, "address": 'address3'},
        {"name": "Patient 4", "gender": "F", "birthdate": "1994-04-04", "no_ktp": 9994, "address": 'address4'},
    ]
    for patient_data in patient_datas:
        post_response = client.post('/patients', json=patient_data)
        assert post_response.status_code == 200
        assert message in post_response.data


def test_post_registered_patients(client):
    test_post_patients(client)

    registered_patient_data = {"name": "Patient 1", "gender": "M", "birthdate": "1991-01-01", "no_ktp": 9991, "address": 'address1'}
    post_response = client.post('/patients', json=registered_patient_data)
    message = b'Failed. ID card number has already been registered.'
    assert post_response.status_code == 200
    assert message in post_response.data


def test_get_patients(client):
    test_post_patients(client)

    get_all_response = client.get('/patients')
    get_all_response_data = data_string_into_dict(get_all_response)
    assert len(get_all_response_data['patients']) == 4
    assert get_all_response.status_code == 200


def test_get_an_patient(client):
    test_post_patients(client)

    patient_names = ['Patient 1', 'Patient 2', 'Patient 3', 'Patient 4']
    for id, patient_name in enumerate(patient_names):
        get_response = client.get(f'/patients/{id+1}')
        get_response_data = data_string_into_dict(get_response)['patient']
        assert get_response_data['name'] == f'{patient_name}'
        assert get_response.status_code == 200


def test_update_an_patient(client):
    test_post_patients(client)

    new_patient3_data = {"name": "Patient 3 New", "gender": "M", "birthdate": "2003-03-03", "no_ktp": 9933, "address": 'new address3'}
    update_response = client.put('/patients/3', json=new_patient3_data)
    assert update_response.status_code == 200

    get_response = client.get('/patients/3')
    get_response_data = data_string_into_dict(get_response)['patient']
    assert get_response_data['name'] == new_patient3_data['name']


def test_delete_an_patient(client):
    test_post_patients(client)

    delete_response = client.delete('/patients/3')
    assert delete_response.status_code == 200

    get_all_response = client.get('/patients')
    get_all_response_data = data_string_into_dict(get_all_response)['patients']
    assert len(get_all_response_data) == 3
    patient_names = [patient_data['name'] for patient_data in get_all_response_data]
    assert 'Patient 1' in patient_names
    assert 'Patient 2' in patient_names
    assert 'Patient 3' not in patient_names
    assert 'Patient 4' in patient_names