import pytest
import requests
import urllib3
from client import create_warehouse, convert_image_file_to_b64_string


def test_create_warehouse():
    result = create_warehouse()
    expected = {'medical_title': '',
                'patient_name': '',
                'ecg_des': '',
                'heart_rate': '0',
                'ecg_image': '',
                'MRI': '0',
                'medical_image': '',
                'medical_des': '',
                'ecg_title': ''}
    assert result == expected


def test_add_medical_image():
    test_dict = create_warehouse()
    test_dict1 = create_warehouse()
    from client import add_medical_image
    filename = "duke_image_for_client_and_server_test.jpg"
    title1 = "Required: Give it a file name to upload"
    title = "Duke"
    des = "Duke chapel front."
    medical_image = convert_image_file_to_b64_string(filename)
    add_medical_image(filename, test_dict, title, des)
    add_medical_image(filename, test_dict1, title1, des)
    result = test_dict
    expected = {'medical_title': title,
                'patient_name': '',
                'ecg_des': '',
                'heart_rate': '0',
                'ecg_image': '',
                'MRI': '0',
                'medical_image': medical_image,
                'medical_des': des,
                'ecg_title': ''}
    result1 = test_dict1
    expected1 = {'medical_title': "duke_image_for_client_and_server_test.jpg",
                 'patient_name': '',
                 'ecg_des': '',
                 'heart_rate': '0',
                 'ecg_image': '',
                 'MRI': '0',
                 'medical_image': medical_image,
                 'medical_des': des,
                 'ecg_title': ''}
    assert result == expected
    assert result1 == expected1


def test_add_ecg_trace():
    from client import add_ecg_trace
    filename = "duke_image_for_client_and_server_test.jpg"
    rate = "80"
    test_dict = create_warehouse()
    test_dict1 = create_warehouse()
    title = "Duke Campus"
    title1 = "Required: Give it a file name to upload"
    des = "A nice place."
    ecg_image = convert_image_file_to_b64_string(filename)
    add_ecg_trace(filename, rate, test_dict, title, des)
    add_ecg_trace(filename, rate, test_dict1, title1, des)
    result = test_dict
    result1 = test_dict1
    expected = {'medical_title': '',
                'patient_name': '',
                'ecg_des': des,
                'heart_rate': '80',
                'ecg_image': ecg_image,
                'MRI': '0',
                'medical_image': '',
                'medical_des': '',
                'ecg_title': title}
    expected1 = {'medical_title': '',
                 'patient_name': '',
                 'ecg_des': des,
                 'heart_rate': '80',
                 'ecg_image': ecg_image,
                 'MRI': '0',
                 'medical_image': '',
                 'medical_des': '',
                 'ecg_title': "duke_image_for_client_and_server_test.jpg"}
    assert result == expected
    assert result1 == expected1


def test_add_mri_name():
    from client import add_mri_name
    mri_1 = ""
    mri_2 = "mri"
    mri_3 = "123"
    mri_correct = "321"
    mri2 = "321"
    test_dict = create_warehouse()
    name = "test_patient"
    result1 = add_mri_name(mri_1, mri2, name, test_dict)
    expected1 = "empty"
    assert result1 == expected1

    result2 = add_mri_name(mri_2, mri2, name, test_dict)
    expected2 = "not digit"
    assert result2 == expected2

    result3 = add_mri_name(mri_3, mri2, name, test_dict)
    expected3 = 1
    assert result3 == expected3

    # remove the influence of previous test
    test_dict = create_warehouse()
    result4 = add_mri_name(mri_correct, mri2, name, test_dict)
    expected4 = 0
    assert result4 == expected4 and \
           test_dict["MRI"] == "321" and \
           test_dict["patient_name"] == "test_patient"


def test_ecg_logging():
    from testfixtures import LogCapture
    from server import logging
    with LogCapture() as log_c:
        logging(0, "a log")
    log_c.check(("root", "INFO", "a log"))


# The uploader function (uploader()) and it's exceptions won't be tested.
# This function is nothing but
# a post request to the server and the exceptions are handling situations like
# The offline situation and connection problems of the server. The return value
# depends on the status of the server(for example online or not which is
# unsure)
