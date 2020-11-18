import pytest
from server import init_db
from scratch_db import Patient


init_db()


def test_add_new_patient():
    from server import add_new_patient
    test_time = "2020-11-16 09:58:19.250418"
    test_in_data1 = {"patient_name": "",
                     "MRI": "123",
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data2 = {"patient_name": "Apple",
                     "MRI": "123",
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data3 = {"patient_name": "Orange",
                     "MRI": "123",
                     "medical_image": "b64_string",
                     "medical_title": "aaa",
                     "medical_des": "bbb",
                     "heart_rate": "90",
                     "ecg_image": "b_64_string2",
                     "ecg_title": "ddd",
                     "ecg_des": "fff"}
    answer1 = add_new_patient(test_in_data1, test_time)
    assert (answer1.MRI == 123 and answer1.name is None and
            answer1.ECG_record == [] and answer1.medical_image == [])
    answer1.delete()
    answer2 = add_new_patient(test_in_data2, test_time)
    assert (answer2.MRI == 123 and answer2.name == "Apple" and
            answer2.ECG_record == [] and answer2.medical_image == [])
    answer2.delete()
    answer3 = add_new_patient(test_in_data3, test_time)
    medical = [{"filename": "aaa", "file_des": "bbb", "image": "b64_string"}]
    ECG = [
        {"filename": "ddd", "file_des": "fff", "heart rate": "90",
         "ECG image": "b_64_string2", "time": "2020-11-16 09:58:19.250418"}
    ]
    assert (answer3.MRI == 123 and answer3.name == "Orange" and
            answer3.ECG_record == ECG and answer3.medical_image == medical)
    answer3.delete()


def test_update_patient_inform():
    from server import add_new_patient, update_patient_inform
    test_time = "2020-11-16 09:58:19.250418"
    test_in_data1 = {"patient_name": "",
                     "MRI": "123",
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data2 = {"patient_name": "Apple",
                     "MRI": "123",
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data3 = {"patient_name": "Orange",
                     "MRI": "123",
                     "medical_image": "b64_string",
                     "medical_title": "aaa",
                     "medical_des": "bbb",
                     "heart_rate": "90",
                     "ecg_image": "b_64_string2",
                     "ecg_title": "ddd",
                     "ecg_des": "fff"}
    base_patient = add_new_patient(test_in_data1, test_time)
    answer1 = update_patient_inform(test_in_data1, test_time, base_patient)
    assert (answer1.MRI == 123 and answer1.name is None and
            answer1.ECG_record == [] and answer1.medical_image == [])
    answer1.delete()
    base_patient = add_new_patient(test_in_data2, test_time)
    answer2 = update_patient_inform(test_in_data2, test_time, base_patient)
    assert (answer2.MRI == 123 and answer2.name == "Apple" and
            answer2.ECG_record == [] and answer2.medical_image == [])
    answer2.delete()
    base_patient = add_new_patient(test_in_data3, test_time)
    answer3 = update_patient_inform(test_in_data3, test_time, base_patient)
    medical = {"filename": "aaa", "file_des": "bbb", "image": "b64_string"}
    ECG = {"filename": "ddd", "file_des": "fff", "heart rate": "90",
           "ECG image": "b_64_string2", "time": "2020-11-16 09:58:19.250418"}
    assert (answer3.MRI == 123 and answer3.name == "Orange" and
            answer3.ECG_record[-1] == ECG and
            answer3.medical_image[-1] == medical)
    answer3.delete()


def test_validate_post_input():
    from server import validate_post_input
    expected_key = ["patient_id", "attending_username", "patient_age"]
    expected_types = [int, str, int]

    in_data1 = {"patient_id": "110",
                "attending_username": "Kobe",
                "patient_age": 99}
    expected1 = "patient_id key value has wrong variable type"
    result1 = validate_post_input(in_data1, expected_key, expected_types)
    assert result1 == expected1

    in_data2 = {"id": "110",
                "attending_username": "Kobe",
                "patient_age": 99}
    expected2 = "patient_id key not found in input"
    result2 = validate_post_input(in_data2, expected_key, expected_types)
    assert result2 == expected2


def test_validate_isdigit():
    from server import validate_isdigit
    key = "key"
    in_data1 = {"key": ""}
    in_data2 = {"key": "123false"}
    in_data3 = {"key": "123"}
    answer1 = validate_isdigit(in_data1, key)
    answer2 = validate_isdigit(in_data2, key)
    answer3 = validate_isdigit(in_data3, key)
    expected1 = "key is empty!"
    expected2 = "key value is not a numerical string"
    expected3 = True
    assert (answer3 == expected3 and answer2 == expected2 and
            answer1 == expected1)


def test_add_patient_to_data_base():
    from server import add_patient_to_data_base
    from server import find_correct_patient
    test_time = "2020-11-16 09:58:19.250418"
    test_in_data = {"patient_name": "Orange",
                    "MRI": "123",
                    "medical_image": "b64_string",
                    "medical_title": "aaa",
                    "medical_des": "bbb",
                    "heart_rate": "90",
                    "ecg_image": "b_64_string2",
                    "ecg_title": "ddd",
                    "ecg_des": "fff"}
    answer1 = add_patient_to_data_base(test_in_data, test_time)
    expected1 = "Patient: 123 successfully added."
    answer2 = add_patient_to_data_base(test_in_data, test_time)
    expected2 = "Patient: 123 information successfully updated."
    patient = find_correct_patient(123)
    patient.delete()


def test_process_new_patient():
    from server import process_new_patient
    from server import find_correct_patient
    test_time = "2020-11-16 09:58:19.250418"
    test_in_data1 = {"patient_name": "",
                     "MRI": 123,
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data2 = {"patient_name": "Apple",
                     "MRI": "123hello",
                     "medical_image": "",
                     "medical_title": "",
                     "medical_des": "",
                     "heart_rate": "",
                     "ecg_image": "",
                     "ecg_title": "",
                     "ecg_des": ""}
    test_in_data3 = {"patient_name": "Orange",
                     "MRI": "123",
                     "medical_image": "b64_string",
                     "medical_title": "aaa",
                     "medical_des": "bbb",
                     "heart_rate": "90",
                     "ecg_image": "b_64_string2",
                     "ecg_title": "ddd",
                     "ecg_des": "fff"}
    answer1 = process_new_patient(test_in_data1, test_time)
    answer2 = process_new_patient(test_in_data2, test_time)
    answer3 = process_new_patient(test_in_data3, test_time)
    answer4 = process_new_patient(test_in_data3, test_time)
    expected1 = ('MRI key value has wrong variable type', 400)
    expected2 = ('MRI value is not a numerical string', 400)
    expected3 = ('Patient: 123 successfully added.', 200)
    expected4 = ('Patient: 123 information successfully updated.', 200)
    assert (answer4 == expected4 and answer3 == expected3 and
            answer2 == expected2 and answer1 == expected1)
    patient = find_correct_patient(123)
    patient.delete()


def make_temp_db():
    global test_data1
    test_data1 = "ecgimage1b64str"
    test_data2 = "ecgimage2b64str"
    test_data3 = "ecgimage3b64str"
    test_data4 = "ecgimage4b64str"

    medical_image1 = "medicalimage1b64str"
    medical_image2 = "medicalimage2b64str"

    global ECG1
    ECG1 = [{"filename": "test_data1.jpg", "heart rate": 200,
             "ECG image": test_data1, "time": "2020-10-10"}
            ]
    ECG2 = [{"filename": "test_data1.jpg", "heart rate": 200,
             "ECG image": test_data1, "time": "2020-10-10"},
            {"filename": "test_data2.jpg", "heart rate": 210,
             "ECG image": test_data2, "time": "2020-11-11"}
            ]
    ECG3 = [{"filename": "test_data1.jpg", "heart rate": 200,
             "ECG image": test_data1, "time": "2020-10-10"},
            {"filename": "test_data2.jpg", "heart rate": 210,
             "ECG image": test_data2, "time": "2020-11-11"},
            {"filename": "test_data3.jpg", "heart rate": 220,
             "ECG image": test_data3, "time": "2020-12-12"}
            ]
    ECG4 = [{"filename": "test_data1.jpg", "heart rate": 200,
             "ECG image": test_data1, "time": "2020-10-10"},
            {"filename": "test_data2.jpg", "heart rate": 210,
             "ECG image": test_data2, "time": "2020-11-11"},
            {"filename": "test_data3.jpg", "heart rate": 220,
             "ECG image": test_data3, "time": "2020-12-12"},
            {"filename": "test_data4.jpg", "heart rate": 230,
             "ECG image": test_data4, "time": "2020-13-13"}
            ]

    global medical1
    medical1 = [{"filename": "meet doctor.jpg", "image": medical_image1}
                ]
    medical2 = [{"filename": "meet doctor.jpg", "image": medical_image1},
                {"filename": "go hospital.png", "image": medical_image2}
                ]

    global patient1
    patient1 = Patient(MRI=1000, name="patient1",
                       ECG_record=ECG1, medical_image=medical1)

    global patient2
    patient2 = Patient(MRI=1100, name='patient2',
                       ECG_record=ECG2, medical_image=medical2)

    global patient3
    patient3 = Patient(MRI=1200, name='patient3',
                       ECG_record=ECG3, medical_image=medical1)

    global patient4
    patient4 = Patient(MRI=1300, name="patient4",
                       ECG_record=ECG4, medical_image=medical2)


make_temp_db()


def test_get_patient_MRI_list():
    from server import get_patient_MRI_list
    # patient1.save()
    # patient2.save()
    # patient3.save()
    # patient4.save()
    result = get_patient_MRI_list()
    MRI_list = []
    for patient in Patient.objects.raw({}):
        MRI_list.append(patient.MRI)
    print(result)
    expected = MRI_list, 200
    assert expected == result
    # patient1.delete()
    # patient2.delete()
    # patient3.delete()
    # patient4.delete()


def test_make_info_list():
    from server import make_info_list
    patient1.save()
    result = make_info_list(1000)
    expected = ['Medical Record Number: 1000', 'Patient Name: patient1',
                'Latest Heart Rate: 200', 'ecgimage1b64str',
                'Uploaded Time: 2020-10-10'], 200
    assert result == expected
    patient1.delete()


def test_find_correct_patient():
    from server import find_correct_patient

    patient1.save()
    result1 = find_correct_patient(1000)
    global ECG1
    global medical1
    expected1 = {"MRI": 1000,
                 "name": "patient1",
                 "ECG_record": ECG1,
                 "medical_image": medical1
                 }
    assert expected1["MRI"] == result1.MRI
    assert expected1["name"] == result1.name
    assert expected1["ECG_record"] == result1.ECG_record
    assert expected1["medical_image"] == result1.medical_image
    patient1.delete()

    result2 = find_correct_patient(9999)
    expected2 = False
    assert expected2 == result2


def test_make_patient_MRI_str():
    from server import make_patient_MRI_str, find_correct_patient

    patient1.save()
    MRI_number = patient1.MRI
    patient_temp = find_correct_patient(MRI_number)
    result = make_patient_MRI_str(patient_temp)
    expected = "Medical Record Number: 1000"
    assert expected == result
    patient1.delete()


def test_make_patient_name_str():
    from server import make_patient_name_str, find_correct_patient

    patient1.save()
    MRI_number = patient1.MRI
    patient_temp = find_correct_patient(MRI_number)
    result = make_patient_name_str(patient_temp)
    expected = "Patient Name: patient1"
    assert expected == result
    patient1.delete()


def test_make_patient_latest_hr_str():
    from server import make_patient_latest_hr_str, find_correct_patient
    patient1.save()
    MRI_number = patient1.MRI
    patient_temp = find_correct_patient(MRI_number)
    result = make_patient_latest_hr_str(patient_temp)
    expected = "Latest Heart Rate: 200"
    assert expected == result
    patient1.delete()


def test_make_patient_latest_ECG_image_str():
    from server import make_patient_latest_ECG_image_str,\
        find_correct_patient
    patient1.save()
    MRI_number = patient1.MRI
    patient_temp = find_correct_patient(MRI_number)
    result = make_patient_latest_ECG_image_str(patient_temp)
    expected = test_data1
    assert expected == result
    patient1.delete()


def test_make_patient_uploaded_time_str():
    from server import make_patient_uploaded_time_str,\
        find_correct_patient
    patient1.save()
    MRI_number = patient1.MRI
    patient_temp = find_correct_patient(MRI_number)
    result = make_patient_uploaded_time_str(patient_temp)
    expected = "Uploaded Time: 2020-10-10"
    assert expected == result
    patient1.delete()


def test_get_patient_ECG_trace_list():
    from server import get_patient_ECG_trace_list

    patient2.save()
    MRI_number = patient2.MRI
    result = get_patient_ECG_trace_list(MRI_number)
    expected = ['2020-10-10'], 200
    assert expected == result
    patient2.delete()


def test_return_patient_another_ECG_image():
    from server import return_patient_another_ECG_image

    patient2.save()
    MRI_number = patient2.MRI
    timestamp = patient2.ECG_record[-1]["time"]
    result = return_patient_another_ECG_image(MRI_number, timestamp)
    expected = 'ecgimage2b64str', 200
    assert expected == result
    patient2.delete()


def test_make_patient_another_ECG_image_str():
    from server import make_patient_another_ECG_image_str,\
        find_correct_patient

    patient2.save()
    MRI_number = patient2.MRI
    patient_temp = find_correct_patient(MRI_number)
    timestamp = patient2.ECG_record[-1]["time"]
    result = make_patient_another_ECG_image_str(patient_temp, timestamp)
    expected = 'ecgimage2b64str'
    assert expected == result
    patient2.delete()


def test_get_patient_medical_image_list():
    from server import get_patient_medical_image_list

    patient3.save()
    MRI_number = patient3.MRI
    result = get_patient_medical_image_list(MRI_number)
    expected = (['meet doctor.jpg'], 200)
    assert expected == result
    patient3.delete()


def test_return_medical_image():
    from server import return_medical_image

    patient3.save()
    MRI_number = patient3.MRI
    filename = patient3.medical_image[-1]["filename"]
    result = return_medical_image(MRI_number, filename)
    expected = "medicalimage1b64str", 200
    assert expected == result
    patient3.delete()


def test_make_patient_medical_image_str():
    from server import make_patient_medical_image_str, \
        find_correct_patient

    patient3.save()
    MRI_number = patient3.MRI
    patient_temp = find_correct_patient(MRI_number)
    filename = patient3.medical_image[-1]["filename"]
    result = make_patient_medical_image_str(patient_temp, filename)
    expected = "medicalimage1b64str"
    assert expected == result
    patient3.delete()


if __name__ == '__main__':
    test_get_patient_MRI_list()
