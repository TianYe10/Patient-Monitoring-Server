from flask import Flask, jsonify, request
import logging
import datetime
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave

from scratch_db import Patient

import json


app = Flask(__name__)


def init_db():
    """ Initialize the MongoDB

    Connect with the MongoDB and initialize the database, show the connecting
    process ("Connecting to database", "Connected")

    Returns:
        None

    """
    logging(0, "The database is initialized")
    print("Connecting to MongoDB...")
    # connect("mongodb+srv://MingzheHu-Duke:201314jin"
    #         "@bme547.d0pad.gcp.mongodb.net"
    #         "/scratch_db?retryWrites=true&w=majority")
    connect("mongodb+srv://YeTian:Tianye19971011!"
            "@bme547.4acg6.mongodb.net/scratch_db?retryWrites=true&w=majority")
    print("Connected")
    print("ran initialization")


@app.route("/api/patient_MRI", methods=["GET"])
def patient_MRI_list():
    """Receive the 'GET' request for getting patients' all
    medical record numbers in the database in a jsonified list,
    each element in the list is a MRI number

    The 'GET' request is send by a client, targeting all available records
    of patients' medical record numbers. The function returns the string
    of medical record number list, along with the corresponding status code.

    Args:
        None

    Returns:
        str, int: A string that includes all content of the of a list of
        patient's medical record numbers. The int is is status code of the
        server, where 200 represents a succeess and 400 represents a server
        error. Actually it can only be 200 here if  the request is normally
        processed with no code error.
    """
    answer, server_status = get_patient_MRI_list()
    return jsonify(answer), server_status


def get_patient_MRI_list():
    """Collect and return a jsonified list of all MRI in database

    When the function is ran, all patients in the databse will be
    traversed and the MRI number of each of them will be appended
    into a list to return.

    Args:
        None

    Returns:
        list: a jsonified list that contains all available MRI numbers
        in the database, each of which is a single element of the
        string
        int: the correct status code
    """
    MRI_list = []
    for patient in Patient.objects.raw({}):
        MRI_list.append(patient.MRI)
    return MRI_list, 200


@app.route("/api/display/info/<MRI_number>", methods=["GET"])
def patient_info(MRI_number):
    """Receive the 'GET' request for getting a jsonified list
    selected patient's MRI, name, latest heart rate, latest ECG image
    and its uploaded time

    The 'GET' request is send by a client, targeting the information of a
    specific patient which is determined by the sent MRI number. The function
    returns the string of a list of all wanted info, along with the
    corresponding status code.

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        str, int: A string that includes all content of the of a list of
        patient's information. The int is is status code of the
        server, where 200 represents a succeess and 400 represents a server
        error. Actually it can only be 200 here if  the request is normally
        processed with no code error.
    """
    answer, server_status = make_info_list(MRI_number)
    return jsonify(answer), server_status


def make_info_list(MRI_number):
    """Collect and return a jsonified list of a patient's
    latest information, which has a length of 5 and different
    elements are different strings that contain one aspect of
    info

    When the function is ran, a patient is selected by the MRI,
    and then all his info, which includes MRI, name, latest heart rate,
    latest ECG image(in b64 string) and the uploaed time, will
    be contained in a string which is in length of 5

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        list: a jsonified list that contains all latest info of
        a selected patient in the database. Every different
         element of the string is showing one aspect of info
        int: the correct status code
    """
    patient = find_correct_patient(MRI_number)
    number = make_patient_MRI_str(patient)
    name = make_patient_name_str(patient)
    latest_hr = make_patient_latest_hr_str(patient)
    latest_ecg_img = make_patient_latest_ECG_image_str(patient)
    time = make_patient_uploaded_time_str(patient)
    info_list = [number, name, latest_hr, latest_ecg_img, time]
    return info_list, 200

# @app.route("/api/display/MRI/<MRI_number>", methods=["GET"])
# def patient_MRI(MRI_number):
#     answer, server_status = return_patient_MRI(MRI_number)
#     return answer, server_status
#
#
# def return_patient_MRI(MRI_number):
#     correct_patient = find_correct_patient(MRI_number)
#     # convert_timestamp_type(correct_patient)
#     patient_info_str = make_patient_MRI_str(correct_patient)
#     # patient_ECG_image = make_ECG_image_str(correct_patient)
#     return jsonify(patient_info_str), 200
#     # return "yes correct", 200


def find_correct_patient(MRI_number):
    """Determine a patient in the database by a MRI number

    This function serves as a necessary step for many other
    functions to call. When this function is ran, a patient class
    in the database is selected by the MRI.
    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        class: a specific patient class in the database
        (or bool: False that indicates not being able to find
        the target patient)
    """
    MRI = int(MRI_number)
    # try:
    #     patient = Patient.objects.raw({"MRI": 1}).first()
    # except pymodm_errors.DoesNotExist:
    #     return False
    for patient in Patient.objects.raw({}):
        if patient.MRI == MRI:
            return patient
    return False
#
#
# # def convert_timestamp_type(patient):
# #     if type(patient.time) is not str:
# #         patient.time = str(patient.time)
# #         patient.save()


def make_patient_MRI_str(patient):
    """Make up a string to show a patient's MRI info

    When the function is ran, the targeted patient's
    MRI string is make up with another statement string
    to contain the information of MRI number

    Args:
        class: a specific patient class in the database

    Returns:
        str: contains the MRI number of the patient and its
        relevant statement
    """
    patient_MRI_str = "Medical Record Number: " + str(patient.MRI)
# "Patient Name: ": patient.name,
# "Latest Heart Rate: ": patient.ECG_record[-1]["heart rate"],
# # "Latest ECG Image": patient.ECG_record[-1]["ECG image"],
# "Uploaded Time": patient.ECG_record[-1]["time"]}
    return patient_MRI_str


# @app.route("/api/display/name/<MRI_number>", methods=["GET"])
# def patient_name(MRI_number):
#     answer, server_status = return_patient_name(MRI_number)
#     return answer, server_status
#
#
# def return_patient_name(MRI_number):
#     correct_patient = find_correct_patient(MRI_number)
#     patient_name_str = make_patient_name_str(correct_patient)
#     return jsonify(patient_name_str), 200
#
#
def make_patient_name_str(patient):
    """Make up a string to show a patient's name

    When the function is ran, the targeted patient's
    name string is make up with another statement string
    to contain the information of patient's full name

    Args:
        class: a specific patient class in the database

    Returns:
        str: contains the full name of the patient and its
        relevant statement
    """
    if patient.name is not None:
        patient_name_str = "Patient Name: " + patient.name
        return patient_name_str
    else:
        return "Patient name:"
#
#
# @app.route("/api/display/latest_hr/<MRI_number>", methods=["GET"])
# def patient_latest_hr(MRI_number):
#     answer, server_status = return_patient_latest_hr(MRI_number)
#     return answer, server_status
#
#
# def return_patient_latest_hr(MRI_number):
#     correct_patient = find_correct_patient(MRI_number)
#     patient_latest_hr_str = make_patient_latest_hr_str(correct_patient)
#     return jsonify(patient_latest_hr_str), 200


def make_patient_latest_hr_str(patient):
    """Make up a string to show a patient's most recent
    heart rate information

    When the function is ran, the targeted patient's latest heart
    rate string is make up with another statement string
    to contain the information

    Args:
        class: a specific patient class in the database

    Returns:
        str: contains the latest heart rate of the patient and its
        relevant statement
    """
    if patient.ECG_record != []:
        patient_latest_hr_str = "Latest Heart Rate: " + \
                                str(patient.ECG_record[-1]["heart rate"])
        return patient_latest_hr_str
    else:
        return "Latest Heart Rate:"
#
#
# @app.route("/api/display/latest_ECG_image/<MRI_number>", methods=["GET"])
# def patient_latest_ECG_image(MRI_number):
#     answer, server_status = return_patient_latest_ECG_image(MRI_number)
#     return answer, server_status


def make_patient_latest_ECG_image_str(patient):
    """Get the b64 string of the patient's latest ECG image

    When the function is ran, the targeted patient's most recent
     ECG record is found and the b64 string for the latest ECG
     trace image is returned

    Args:
        class: a specific patient class in the database

    Returns:
        str: he b64 string for the latest ECG trace image
    """
    if patient.ECG_record != []:
        patient_latest_ECG_image_str = patient.ECG_record[-1]["ECG image"]
        return patient_latest_ECG_image_str
    else:
        return ""
#
#
# @app.route("/api/display/uploaded_time/<MRI_number>", methods=["GET"])
# def patient_uploaded_time(MRI_number):
#     answer, server_status = return_patient_uploaded_time(MRI_number)
#     return answer, server_status
#
#


def make_patient_uploaded_time_str(patient):
    """Make up a string to show a patient's time for the most
    recent ECG image submission

    When the function is ran, the targeted patient's
    most recent time string of the latest ECG record is made up
    with another statement string to contain the information
    of the latest uploaded time

    Args:
        class: a specific patient class in the database

    Returns:
        str: contains the uploaded time of the patient and its
        relevant statement
    """
    if patient.ECG_record != []:
        patient_uploaded_time_str = "Uploaded Time: " + \
                                    patient.ECG_record[-1]["time"]
        return patient_uploaded_time_str
    else:
        return "Uploaded Time:"


@app.route("/api/patient_ECG_trace/<MRI_number>", methods=["GET"])
def patient_ECG_trace_list(MRI_number):
    """Receive the 'GET' request for getting a selected patient's timestamps
    of ECG images(except the latest one). The list contains strings as elements,
    each of which indicates the info of timestamp for every ECG image

    The 'GET' request is send by a client, targeting the timestamps of a
    specific patient's ECG trace images(except the latestone) which is
    determined by the sent MRI number. The function  returns the string
    of a list of all wanted info, along with the corresponding status code.

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        str, int: A string that includes all content of the of a list of
        patient's ECG image timestamps(except the latest one). The int
        is status code of the server, where 200 represents a succeess and
        400 represents a server error. Actually it can only be 200 here if
        the request is normally processed with no code error.
    """
    answer, server_status = get_patient_ECG_trace_list(MRI_number)
    return jsonify(answer), server_status


def get_patient_ECG_trace_list(MRI_number):
    """Find the target patient in the database and make a list of
    patient's timestamps of ECG images(except the latest one)

    By calling find_correct_patient(MRI), the function finds a
    specific patient in the database and then all of that patient's
    ECG records' timestamps are integrated to a list. The list is
    returned after being jsonified.

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        list: a jsonified list with each of its elements indicates
        a timestamp for a selected patient's ECG record(except the
        latest one)
        int: the correct status code
    """
    trace_list = []
    patient = find_correct_patient(MRI_number)
    for record in patient.ECG_record[:-1]:
        trace_list.append(record["time"])
    return trace_list, 200


@app.route("/api/display/another_ECG_image/<MRI_number>/<timestamp>",
           methods=["GET"])
def another_latest_ECG_image(MRI_number, timestamp):
    """Receive the 'GET' request for getting a selected ECG image of
    a specific patient, which is returned in b64 string

    The 'GET' request is send by a client, targeting the b64 string of
    a  specific ECG image. The owner patient of that ECG image is
    determined  by the sent MRI number and the ECG image is determined
    by the corresponding timestamp. The function returns the string of
    a list of all wanted info, along with the status code.

    Args:
        int: the MRI number for the targeted patient in database
        str: a string of timestamp to select a specific ECG image

    Returns:
        str, int: A b64 string of the wanted image of the targeted patient.
        The int is is status code of the server, where 200 represents a
        success and 400 represents a server error. Actually it can only
        be 200 here if  the request is normally processed with no code error.
    """
    answer, server_status = return_patient_another_ECG_image(MRI_number,
                                                             timestamp)
    return answer, server_status


def return_patient_another_ECG_image(MRI_number, timestamp):
    """Find the target patient and selected ECG image

    MRI_number uniquely determines which patient to know about,
    and the timestamp corresponds an MRI image of that patient by
    calling the function below. The b64 of the chosen image is then
    returned with a status code for success.

    Args:
        int: the MRI number for the targeted patient in database
        str: the timestamp that indicates the wanted ECG image

    Returns:
        str: the b64 string for the selected ECG image
    """
    correct_patient = find_correct_patient(MRI_number)
    patient_another_ECG_image_str = make_patient_another_ECG_image_str(
        correct_patient, timestamp)
    return patient_another_ECG_image_str, 200


def make_patient_another_ECG_image_str(patient, timestamp):
    """Get the b64 string of the chosen ECG image

    The patient determines the specific patient class that is
    targeted and the timestamp uniquely connects the b64 string
    of a ECG image. Then the b64 string of that wanted image
    is returned.

    Args:
        class: a specific patient class in the database
        str: the timestamp that indicates the wanted ECG image

    Returns:
        str: the b64 string for the selected ECG trace image
    """
    for image in patient.ECG_record:
        if image["time"] == timestamp:
            patient_another_ECG_image_str = image["ECG image"]
    return patient_another_ECG_image_str


@app.route("/api/medical_image_list/<MRI_number>", methods=["GET"])
def patient_medical_image_list(MRI_number):
    """Receive the 'GET' request for getting a list of names of all
    available medical images of a selected patient. The elements for
    the list are strings that contain the info of every image's name

    The 'GET' request is send by a client, targeting the names of medical
    images of a specific patient which is determined by the sent MRI
    number. The function  returns the string of a list of all wanted info,
    along with the corresponding status code.

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        str, int: A string that includes all content of the of a list of
        patient's medical images' names. The int is is status code of the
        server, where 200 represents a succeess and 400 represents a server
        error. Actually it can only be 200 here if  the request is normally
        processed with no code error.
    """
    answer, server_status = get_patient_medical_image_list(MRI_number)
    return jsonify(answer), server_status


def get_patient_medical_image_list(MRI_number):
    """Find the target patient in the database and make a list of
    filename strings of patient's medical images

    By calling find_correct_patient(MRI), the function finds a
    specific patient in the database and then all of that patient's
    medical images' filenames are integrated to a list. The list is
    returned after being jsonified.

    Args:
        int: the MRI number for the targeted patient in database

    Returns:
        list: a jsonified list with each of its elements indicates
        a filename string for a selected patient's medical image
        int: the correct status code
    """
    medical_image_list = []
    patient = find_correct_patient(MRI_number)
    for image in patient.medical_image:
        medical_image_list.append(image["filename"])
    return medical_image_list, 200


@app.route("/api/display/medical_image/<MRI_number>/<filename>",
           methods=["GET"])
def find_medical_image(MRI_number, filename):
    """Receive the 'GET' request for getting a selected medical image of
    a specific patient and image is returned in b64 string

    The 'GET' request is send by a client, targeting the b64 string of
    a  specific medical image. The owner patient of that medical image is
    determined  by the sent MRI number and the medical image is determined
    by the corresponding name. The function returns the string of a list
    of all wanted info, along with the status code.

    Args:
        int: the MRI number for the targeted patient in database
        str: a string of image name to select a specific medical image

    Returns:
        str, int: A b64 string of the wanted image of the targeted patient.
        The int is is status code of the server, where 200 represents a
        success and 400 represents a server error. Actually it can only
        be 200 here if  the request is normally processed with no code error.
    """
    answer, server_status = return_medical_image(MRI_number, filename)
    return answer, server_status


def return_medical_image(MRI_number, filename):
    """Find the target patient and selected medical image

    MRI_number uniquely determines which patient to know about,
    and the filename corresponds a medical image of that patient by
    calling the function below. The b64 of the chosen image is then
    returned with a status code for success.

    Args:
        int: the MRI number for the targeted patient in database
        str: the filename that indicates the wanted ECG image

    Returns:
        str: the b64 string for the selected medical image
        int: the correct status code
    """
    correct_patient = find_correct_patient(MRI_number)
    patient_medical_image_str = make_patient_medical_image_str(correct_patient,
                                                               filename)
    return patient_medical_image_str, 200


def make_patient_medical_image_str(patient, filename):
    """Get the b64 string of the chosen medical image

    The patient determines the specific patient class that is
    targeted and the filename uniquely connects the b64 string
    of a chosen medical image. Then the b64 string of that wanted image
    is returned.

    Args:
        class: a specific patient class in the database
        str: the filename that indicates the wanted ECG image

    Returns:
        str: the b64 string for the selected medical image
    """
    for image in patient.medical_image:
        if image["filename"] == filename:
            patient_medical_image_str = image["image"]
    return patient_medical_image_str


@app.route("/api/upload", methods=["POST"])
def post_new_patient():
    """This is the function that receive the post request fom patient client

    The in_data is sent by the patient side client. It is a dictionary with the
    following keys:
    "patient_name" (str): the uploaded patient's name
    "MRI" (str): the medical record number uploaded, this value is unique
    "medical_image" (str): the medial image in the form of a b64_string
    "medical_title": The user defined filename of the medical image
    "medical_des": The user defined the description of the uploaded medical
    image
    "heart_rate": The heart rate in BPM analyzed from the ecg .csv file
    "ecg_image": The ecg_trace image generated after the analysis of the ecg
    trace data
    "ecg_title": The user defined file name of the ecg image
    "ecg_des": The user defined description of the ecg image
    This function will also take down the time information when the server
    received this post request.

    Returns:
        str, int: The string will indicate if the request succeed. It might
        indicate if the input has valid keys and corresponding types. If the
        input mri is a pure numeric string, if the new patient is added or the
        existing patient's information is updated
        The int is is status code of the server, where 200 represent succeed
        and 400 represent a bad post request

    """
    # Receive request data
    logging(0, "Post request to upload patient data received!")
    in_data = request.get_json()
    time = str(datetime.datetime.now())
    answer, server_status = process_new_patient(in_data, time)
    return answer, server_status


def process_new_patient(in_data, time):
    """Process the submitted patient information

    This function will process and examine the patient data stored in the
    in_data dictionary. It will first check if the dictionary includes all
    the expected keys. Later it will check if all the keys are in the expected
    types. Then, it will call the add_or_update function to either add a new
    patient with the information or update the existing patient's information
    in the MongoDB.

    Args:
        in_data (dict): The dictionary sent by the patient client and received
        in server that includes all the uploaded information of a patient.
        time (str): The time of when post request in the server corresponding
        to a specific patient.

    Returns:
        str, int: The str will indicate if the input keys and types are valid,
        it will also indicate if the mri number of the input is a pure numeric
        number or not. If the the patient is successfully send to the MongoDB
        it will indicate if there is a new patient is added or it was updating
        information of an existing patient. The detailed returns options can be
        checked according to the sub-functions that return them.
        The int is is status code of the server, where 200 represent succeed
        and 400 represent a bad post request

    """
    expected_key = ["patient_name", "MRI", "medical_image", "medical_title",
                    "medical_des", "heart_rate", "ecg_image", "ecg_title",
                    "ecg_des"]
    expected_types = [str, str, str, str, str, str, str, str, str]
    validate_input = validate_post_input(in_data, expected_key, expected_types)
    if validate_input is not True:
        return validate_input, 400
    validate_digit = validate_isdigit(in_data, "MRI")
    if validate_digit is not True:
        return validate_digit, 400
    # Checking the some in image is not required, this will greatly reduce the
    # speed of the server
    # validate_medical_image = validate_isdigit(in_data["medical_image"])
    # validate_ecg_image = validate_isdigit(in_data["ecg_image"])
    # if validate_medical_image and validate_ecg_image is not True:
    #     return "Image is not correctly encoded!", 400
    add_or_update = add_patient_to_data_base(in_data, time)
    return add_or_update, 200


def add_patient_to_data_base(in_data, time):
    """ Add the patient information to the database together with the timestamp

    This function will first call the find_correct_patient function to check
    if the patient mri number has already existed in the MongoDB. If if it does
    it will update the database according to the in_data information, otherwise
    it will create a new patient recode and save it into the database.

    Args:
        in_data (dict): The dictionary includes the uploaded user's information
        received by the server from the post request
        time (str): The time of when the server received the post request

    Returns:
        str: "Patient: xx successfully added if a new patient is added
        "Patient: xx information successfully updated

    """
    does_exist = find_correct_patient(in_data["MRI"])
    if does_exist is False:
        add_new_patient(in_data, time)
        logging(0, "Patient: {} successfully added.".format(in_data["MRI"]))
        return "Patient: {} successfully added.".format(in_data["MRI"])
    else:
        update_patient_inform(in_data, time, does_exist)
        logging(0, "Patient: {} information"
                " successfully updated.".format(in_data["MRI"]))
        return "Patient: {} information successfully updated.".\
            format(in_data["MRI"])


def add_new_patient(in_data, time):
    """Add a new patient record to the MongoDB

    This function will add a new patient record to the database. It will at
    least add the patient's MRI number. If the patient name does exist, then
    it will also add the patient's name. If the medical image does exist, it
    will add the medical image all together with the title and description with
    it. If the ecg_trace image does exist. It will also add the ecg_trace image
    and the image title and description all together with it. Notice the ecg
    and medical information will be saved as a term of the list, so the
    incoming information will be added to the existing information

    Args:
        in_data(dict): The dictionary sent by the patient client that include
        all the information uploaded by the user
        time (string): The time when the server respond to the post request (
        the receipt time of the ecg trace image and information

    Returns:
        MongoDB class: The newly added patient entry

    """
    name = in_data["patient_name"]
    mri = in_data["MRI"]
    medical_image = in_data["medical_image"]
    medical_title = in_data["medical_title"]
    medical_des = in_data["medical_des"]
    rate = in_data["heart_rate"]
    ecg_image = in_data["ecg_image"]
    ecg_title = in_data["ecg_title"]
    ecg_des = in_data["ecg_des"]
    patient = Patient(MRI=mri)
    if name != "":
        patient.name = name
    if medical_image != "":
        medical = [{"filename": medical_title,
                    "file_des": medical_des,
                    "image": medical_image}]
        patient.medical_image = medical
    if ecg_image != "":
        ecg = [{"filename": ecg_title,
                "file_des": ecg_des,
                "heart rate": rate,
                "ECG image": ecg_image,
                "time": time}]
        patient.ECG_record = ecg
    patient.save()
    return patient


def update_patient_inform(in_data, time, does_exist):
    """Update the information of an existing patient

     This function will update patient record to the database. It will at
     least un change the patient's MRI number. If the medical image does exist,
     append the medical image all together with the title and description.
     If the ecg_trace image does exist. It will also append the ecg_trace image
     and the image title and description all together with it. Notice the ecg
     and medical information will be saved as a term of the list, so the
     incoming information will be added to the existing information

     Args:
         in_data(dict): The dictionary sent by the patient client that include
         all the information uploaded by the user
         time (string): The time when the server respond to the post request (
         the receipt time of the ecg trace image and information

     Returns:
         MongoDB class: The updated user

     """
    medical_image = in_data["medical_image"]
    medical_title = in_data["medical_title"]
    medical_des = in_data["medical_des"]
    rate = in_data["heart_rate"]
    ecg_image = in_data["ecg_image"]
    ecg_title = in_data["ecg_title"]
    ecg_des = in_data["ecg_des"]
    patient = does_exist
    if medical_image != "":
        medical_record = {"filename": medical_title,
                          "file_des": medical_des,
                          "image": medical_image}
        patient.medical_image.append(medical_record)
    if ecg_image != "":
        ecg_record = {"filename": ecg_title,
                      "file_des": ecg_des,
                      "heart rate": rate,
                      "ECG image": ecg_image,
                      "time": time}
        patient.ECG_record.append(ecg_record)
    patient.save()
    return patient


def validate_post_input(in_data, expected_key, expected_types):
    """Validate the input sent by the post request

    This function will first validate if all the expected keys does exist in
    the received dictionary. Then it will also check if the type of the values
    corresponding to each key meet with the requirement for the next steps
    processing.

    Args:
        in_data (dict): The dictionary sent by the patient client which include
        all the information uploaded by users
        expected_key (list): list of strings, indicate what are the keys that
        are expected to exist in the dictionary
        expected_types (list): A list indicate what are the expected types of
        each values corresponding to each keys in the expected keys dictionary

    Returns:
        str: "xx key not found in input" if one all more keys are missing in
        the input dictionary. "xx key has wrong variable type" if one or more
        key values has the wrong type different from what we expected.
        True: If no problem found

    """
    for key, v_type in zip(expected_key, expected_types):
        if key not in in_data.keys():
            logging(1, "{} key not found in input".format(key))
            return "{} key not found in input".format(key)
        if type(in_data[key]) != v_type:
            logging(2, "{} key value has wrong variable type".format(key))
            return "{} key value has wrong variable type".format(key)
    return True


def validate_isdigit(in_data, key):
    """Validate if a key value of a dictionary is a pure numeric string

    This function will check if the the value of a dictionary's key is a string
    that only includes the digits

    Args:
        in_data (dict): The dictionary sent py the patient side client that
        include all the information uploaded by the users
        key (string): The key of the dictionry whose value you want to check.

    Returns:
        str: "xx is empty" if the key value is an empty string. "xx value id
        not a numerical string" if the string also includes chars besides
        digits.
        True: If the string is not empty and only includes digits

    """
    if in_data[key] == "":
        return "{} is empty!".format(key)
    elif in_data[key].isdigit() is False:
        return "{} value is not a numerical string".format(key)
    return True


# def validate_image_format(image):
#     """ Test if image is coded in b64_string
#
#     This function will first try to decode the string and encode it again to
#     see if it can get the original b64_string. If exception happen,
#     that means
#     it is not encoded in b64 string.
#
#     Args:
#         image (str): The string of the input image
#
#     Returns:
#         True: if the image is encoded in b64
#         str : indicate it is not encoded in b64
#
#     """
#     try:
#         return base64.b64encode(base64.b16decode(image)) == image
#     except TypeError:
#         return "The input image is not encoded" \
#                " in the b64 format"


def logging(level, description):
    """Log all the events
    log all the events, user can decide the level and customize the
    description
    Args:
        level (int): the logging level
        description (string): The string add to the log
    Returns:
        None
    """
    import logging
    # only log the level above INFO
    logging.basicConfig(filename="server.log", level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    if level == 0:
        logging.info(description)
    elif level == 1:
        logging.warning(description)
    elif level == 2:
        logging.error(description)
    return


if __name__ == '__main__':
    # The main entrance of the function
    # No main() function is designed so no docstring
    init_db()
    app.run()
