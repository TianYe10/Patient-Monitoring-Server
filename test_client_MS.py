from scratch_db import Patient
from server import init_db


def make_temp_db():

    init_db()

    test_data1 = "ecgimage1b64str"
    test_data2 = "ecgimage2b64str"
    test_data3 = "ecgimage3b64str"
    test_data4 = "ecgimage4b64str"

    medical_image1 = "medicalimage1b64str"
    medical_image2 = "medicalimage2b64str"

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


def test_medical_record_number_list():
    from client_MS import medical_record_number_list
    result = medical_record_number_list()
    MRI_list = []
    for patient in Patient.objects.raw({}):
        MRI_list.append(patient.MRI)
    expected = MRI_list
    assert expected == result
    # result_old = medical_record_number_list()
    # patient5 = Patient(MRI=1400, name='patient5')
    # patient5.save()
    #
    # patient6 = Patient(MRI=1500, name="patient6")
    # patient6.save()
    # result_new = medical_record_number_list()
    # expected = result_old.append([1400, 1500])
    # assert expected == result_new
    # patient5.delete()
    # patient6.delete()


def test_display_selected_patient_info():
    from client_MS import display_selected_patient_info
    patient1.save()
    result1 = display_selected_patient_info(1000)
    expected1 = ('Medical Record Number: 1000', 'Patient Name: patient1',
                 'Latest Heart Rate: 200', 'ecgimage1b64str',
                 'Uploaded Time: 2020-10-10')
    assert expected1 == result1
    patient1.delete()

    patient4.save()
    result2 = display_selected_patient_info(1300)
    expected2 = ('Medical Record Number: 1300', 'Patient Name: patient4',
                 'Latest Heart Rate: 230', 'ecgimage4b64str',
                 'Uploaded Time: 2020-13-13')
    assert expected2 == result2
    patient4.delete()


def test_ECG_trace_list():
    from client_MS import ECG_trace_list

    patient4.save()
    result1 = ECG_trace_list(1300)
    expected1 = ['"2020-10-10"', '"2020-11-11"', '"2020-12-12"']
    assert expected1 == result1
    patient4.delete()

    patient2.save()
    result2 = ECG_trace_list(1100)
    expected2 = ['"2020-10-10"']
    assert expected2 == result2
    patient2.delete()

    patient1.save()
    result3 = ECG_trace_list(1000)
    expected3 = ['']
    assert expected3 == result3
    patient1.delete()


def test_display_another_ECG_image():
    from client_MS import display_another_ECG_image

    patient4.save()
    result1 = display_another_ECG_image(1300, "2020-10-10")
    expected1 = 'ecgimage1b64str'
    assert expected1 == result1
    patient4.delete()

    patient3.save()
    result2 = display_another_ECG_image(1200, "2020-11-11")
    expected2 = "ecgimage2b64str"
    assert expected2 == result2
    patient3.delete()


def test_medical_image_list():
    from client_MS import medical_image_list

    patient2.save()
    result1 = medical_image_list(1100)
    expected1 = ['"meet doctor.jpg"', '"go hospital.png"']
    assert expected1 == result1
    patient2.delete()

    patient1.save()
    result2 = medical_image_list(1000)
    expected2 = ['"meet doctor.jpg"']
    assert expected2 == result2
    patient1.delete()

    patient4.save()
    result3 = medical_image_list(1300)
    expected3 = ['"meet doctor.jpg"', '"go hospital.png"']
    assert expected3 == result3
    patient4.delete()


def test_display_medical_image():
    from client_MS import display_medical_image

    patient3.save()
    result1 = display_medical_image(1200, "meet doctor.jpg")
    expected1 = "medicalimage1b64str"
    assert expected1 == result1
    patient3.delete()

    patient4.save()
    result2 = display_medical_image(1300, "go hospital.png")
    expected2 = "medicalimage2b64str"
    assert expected2 == result2
    patient4.delete()


# def delete_temp_db():
#     patient1 = Patient(MRI=1000)
#     patient1.delete()
#
#     patient2 = Patient(MRI=1100)
#     patient2.delete()
#
#     patient3 = Patient(MRI=1200)
#     patient3.delete()
#
#     patient4 = Patient(MRI=1300)
#     patient4.delete()
#
#
# delete_temp_db()
