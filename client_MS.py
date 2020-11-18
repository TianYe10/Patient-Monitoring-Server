import requests
import base64


def medical_record_number_list():
    """ Get the list of all patients' MRI list

    The function sends a 'GET' request to the server, get a
    string that includes all patient's MRI information as well
    as other unnecessary signals and punctuaions. Then it filters
    out only digit elements by using split() function and save
    each of them as a new element into a list to return.

    Args:
        None

    Returns:
        list: A list of all existing medical record numbers
    in the database. Each number is appended as a string element
    into the list. The length of this list is equal to the total
    number of patients.
    """
    r = requests.get("http://127.0.0.1:5000/api/patient_MRI")
    temp_list = r.text[1:-2].split(",")
    MRI_list = []
    for temp in temp_list:
        MRI = (temp)
        MRI_list.append(MRI)
    return MRI_list


def display_selected_patient_info(MRI):
    """ Get a patient's latest information and ECG trace image

     As a very important functionality of the server, the function
     sends a 'GET' request to the server, get a string that includes
     all patient's latest info and ECG image b64 string. Then it
     splits each content by the comma, and returns them separately.

     Args:
         int/str: A integer of medical record number, or a numeric
         string that indicates a medical record number

     Returns:
         str, str, str, str,str, str: 5 separate strings that contain
         patient's information about the medical record number, patient
         name, latest heart rate, latest ECG image(b64 string) and when
         the latest ECG record was updated
     """
    r = requests.get("http://127.0.0.1:5000//api/display/info/" + str(MRI))
    info_list = r.text[1:-2].split(",")
    number = eval(info_list[0])
    name = eval(info_list[1])
    latest_hr = eval(info_list[2])
    latest_ECG_image = eval(info_list[3])
    uploaded_time = eval(info_list[4])

    return number, name, latest_hr, latest_ECG_image, uploaded_time


def save_b64_string_to_file(b64_string, filename):
    """ Open a new document locally to save a b64 string
    as an image file.

    This function serves as an important functionality for
    converting and saving a b64 string to a new image file.
    Also, the user who call this function can determine
    the file name and format of the image file to be saved.

    Args:
        b64_string: the string that contains info for the image
        to be saved
        filename: the string to be the name of saved image file

    Returns:
        None. But a new image file is created in the file path.
    """
    image_bytes = base64.b64decode(b64_string)
    with open(filename, "wb") as out_file:
        out_file.write(image_bytes)


def ECG_trace_list(MRI):
    """ Get a list of patient's ECG images(except the latest one)

    Target a patient in the database by the MRI, use the 'GET' request
    for server to get that patient's all ECG image timestamps(except
    the latest one) and save them to a string.

    Args:
        int/str: A integer of medical record number, or a numeric
         string that indicates a medical record number

    Returns:
        List: A list of the timestamps corresponding to patient's
        every ECG image
    """
    r = requests.get("http://127.0.0.1:5000/api/patient_ECG_trace/" + str(MRI))
    trace_list_str = r.text[1:-2]
    trace_list = trace_list_str.split(",")
    return trace_list  # when empty: ['']  (there always a single quote mark!)


def display_another_ECG_image(MRI, timestamp):
    """ Get the b64 string for a patient's selected ECG image

    Send a 'GET' request to the server, target a patient in the
    database by MRI, then lock a selected ECG image b64 string
    by the unique corresponding timestamp. Finally, returns that
    b64 string as the function output.

    Args:
        int/str: A integer of medical record number, or a numeric
         string that indicates a medical record number
        str: A string which should be the same as a timestamp string
        for a patient in the database

    Returns:
          The wanted b64 string for a specific image of the selected
          patient
    """
    r = requests.get("http://127.0.0.1:5000/api/display/another_ECG_image/" +
                     str(MRI) + "/" + timestamp)
    return r.text


def medical_image_list(MRI):
    """ Get a list of patient's medical images

    Target a patient in the database by the MRI, use the 'GET' request
    for server to get that patient's all medical images' names
    and save them to a string.

    Args:
        int/str: A integer of medical record number, or a numeric
         string that indicates a medical record number

    Returns:
        List: A list of the image names corresponding to patient's
        every medical image
    """
    r = requests.get("http://127.0.0.1:5000/api/medical_image_list/" +
                     str(MRI))
    medical_image_list_str = r.text[1:-2]
    image_list = medical_image_list_str.split(",")
    return image_list


def display_medical_image(MRI, filename):
    """ Get the b64 string for a patient's selected medical image

    Send a 'GET' request to the server, target a patient in the
    database by MRI, then lock a selected ECG image b64 string
    by the unique corresponding string of image name. Finally,
    returns that b64 string as the function output.

    Args:
        int/str: A integer of medical record number, or a numeric
         string that indicates a medical record number
        str: A string which should be the same as a name string
        for a patient in the database

    Returns:
          The wanted b64 string for a specific medical image of
          the selected patient
    """
    r = requests.get("http://127.0.0.1:5000/api/display/medical_image/" +
                     str(MRI) + "/" + filename)
    return r.text


def convert_image_file_to_b64_string(filename):
    """ Get the b64 string for a selected image file

    As a tool function, simply take the filename(of an image)
    that the user wants to convert, open that file,
    read it and turns it into a corresponding b64 string

    Args:
        str: the name of which file the user wants to convert

    Returns:
          The wanted b64 string for an image with a predetermined
          filename
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding="utf-8")
    return b64_string
