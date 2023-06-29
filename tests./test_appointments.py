from .test_login_and_authorization import admin_login, data_string_into_dict
from .test_doctors import test_post_doctors
from .test_patients import test_post_patients

def test_post_appointments(client):
    test_post_doctors(client)
    test_post_patients(client)

    message = b'Success. Your appointment validation process is fulfilled.'
    appointment_datas = [
        { "doctor_id": 1, "patient_id": 1, "datetm": "2023-06-04 15:00:00", "status": "CANCELLED", "diagnose": "diagnose disease A", "notes": "some notes..."},
        { "doctor_id": 1, "patient_id": 2, "datetm": "2023-06-12 15:00:00", "status": "DONE", "diagnose": "diagnose disease A", "notes": "some notes..."},
        { "doctor_id": 2, "patient_id": 3, "datetm": "2023-06-14 15:00:00", "status": "IN_QUEUE", "diagnose": "diagnose disease B", "notes": "some notes..."},
    ]
    for appointment_data in appointment_datas:
        post_response = client.post('/appointments', json=appointment_data)
        assert post_response.status_code == 200
        assert message in post_response.data


def test_working_hours_validation(client):
    test_post_appointments(client)
    
    message = b"Failed. The requested appointment  time is outside the doctor's working hours."
    outside_working_hours_appointment_datas = [
        { "doctor_id": 2, "patient_id": 3, "datetm": "2023-06-15 04:00:00", "status": "IN_QUEUE", "diagnose": "diagnose disease B", "notes": "some notes..."},
        { "doctor_id": 2, "patient_id": 4, "datetm": "2023-06-15 23:00:00", "status": "IN_QUEUE", "diagnose": "diagnose disease B", "notes": "some notes..."},
    ]
    for appointment_data in outside_working_hours_appointment_datas:
        post_response = client.post('/appointments', json=appointment_data)
        assert post_response.status_code == 200
        assert message in post_response.data


def test_booking_validation(client):
    test_post_appointments(client)
    
    message = b'Failed. The requested appointment time has already been booked by another patient.'
    booked_appointment_data = { "doctor_id": 2, "patient_id": 3, "datetm": "2023-06-14 15:00:00", "status": "IN_QUEUE", "diagnose": "diagnose disease B", "notes": "some notes..."}
    post_response = client.post('/appointments', json=booked_appointment_data)
    assert post_response.status_code == 200
    assert message in post_response.data


def test_get_appointments(client):
    test_post_appointments(client)

    get_all_response = client.get('/appointments')
    get_all_response_data = data_string_into_dict(get_all_response)
    assert len(get_all_response_data['appointments']) == 3
    assert get_all_response.status_code == 200


def test_get_an_appointment(client):
    test_post_appointments(client)

    doctor_and_patient_ids = [(1,1), (1,2), (2,3)]
    for id, doctor_and_patient_id in enumerate(doctor_and_patient_ids):
        get_response = client.get(f'/appointments/{id+1}')
        get_response_data = data_string_into_dict(get_response)['appointment']
        assert get_response_data['doctor_id'] == doctor_and_patient_id[0]
        assert get_response_data['patient_id'] == doctor_and_patient_id[1]
        assert get_response.status_code == 200


def test_update_an_appointment(client):
    test_post_appointments(client)

    new_appointment3_data = {"doctor_id": 2, "patient_id": 3, "datetm": "2023-06-14 15:00:00", "status": "DONE", "diagnose": "diagnose disease B", "notes": "some notes..."}
    update_response = client.put('/appointments/3', json=new_appointment3_data)
    assert update_response.status_code == 200

    get_response = client.get('/appointments/3')
    get_response_data = data_string_into_dict(get_response)['appointment']
    assert get_response_data['doctor_id'] == new_appointment3_data['doctor_id']
    assert get_response_data['patient_id'] == new_appointment3_data['patient_id']


def test_delete_an_appointment(client):
    test_post_appointments(client)

    delete_response = client.delete('/appointments/1')
    assert delete_response.status_code == 200

    get_all_response = client.get('/appointments')
    get_all_response_data = data_string_into_dict(get_all_response)['appointments']
    assert len(get_all_response_data) == 2
    appointment_doctor_and_patient_ids = [
        (appointment_data['doctor_id'], appointment_data['patient_id'])
            for appointment_data 
            in get_all_response_data
    ]
    assert (1,1) not in appointment_doctor_and_patient_ids
    assert (1,2) in appointment_doctor_and_patient_ids
    assert (2,3) in appointment_doctor_and_patient_ids