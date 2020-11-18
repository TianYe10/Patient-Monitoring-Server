import requests
import base64
import os
import urllib3


# This function will not be tested
def convert_image_file_to_b64_string(filename):
    """Convert a image file to the corresponding b64_string

    This function will all the b64encode function from the base64 module and
    convert the specified image file to b64_string for saving in data bse and
    transmission. The image file could be either JPEG file or PNG file.

    Args:
        filename (str): The name (path)  of image you want to process

    Returns:
        str : The b64_string that was generated

    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding="utf-8")
    return b64_string


def add_medical_image(filename, dict_in, title, description):
    """Add the medical image information to the dictionary(dict_in)

    The information related to the medical image will be added to the
    dictionary(dict_in). The information includes: user-defined name of the
    medical image, user defined description of the medical image and the image
    itself in the form of a b64_string.

    Args:
        filename (str): The path of the medical image
        dict_in (dict): The global dictionary in the client_gui that store all
        the information to be sent to the server and save in mongoDB
        title (str): The user defined filename of the medical image
        description (str): The user's description of the medical image

    Returns:
        None

    """
    b64_string = convert_image_file_to_b64_string(filename)
    dict_in["medical_image"] = b64_string
    saved_name = os.path.basename(filename)
    saved_name = os.path.splitext(saved_name)[0]
    if title == "Required: Give it a file name to upload":
        title = "{}.jpg".format(saved_name)
    dict_in["medical_title"] = title
    dict_in["medical_des"] = description
    return


def add_ecg_trace(filename, rate,  dict_in, title, description):
    """Add the ecg trace information to the dictionary(dict_in)

    The information related to the ecg trace (after being processed) will be
     added to the dictionary(dict_in). The information includes: user-defined
     name of the ecg trace image, user defined description of the ecg trace
     image, heart rate calculated and the ecg image in the form of a
     b64_string.

    Args:
        filename (str): The path of the .csv file storing the ecg trace data
        rate (str): The calculated heart rate from the .csv file
        dict_in (dict): The global dictionary in the client_gui that store all
        the information to be sent to the server and save in mongoDB
        title (str): The user defined filename of the ecg trace image
        description (str): The user's description of the ecg_trace image

    Returns:
            None

    """
    b64_string = convert_image_file_to_b64_string(filename)
    dict_in["ecg_image"] = b64_string
    dict_in["heart_rate"] = str(rate)
    if title == "Required: Give it a file name to upload":
        title = "{}".format(filename)
    dict_in["ecg_title"] = title
    dict_in["ecg_des"] = description
    return


def add_mri_name(mri, mri2, name, dict_in):
    """Add the mri and patient name strings to the global dictionary

    This function will save the mri and patient name data to the global
    dictionary before they are sending and storing in the mongoDB. it will
    also check if the mri is empty or not a digit. It will also verify if
    the mri information entered the first time and the second time are the
    same or not.

    Args:
        mri (str): The mri input by the users
        mri2 (str): The second mri input from the users to recheck if the
        correct mri is input
        name (str): Patient name input by the users
        dict_in (dict): The global dictionary in the client_gui that store all
        the information to be sent to the server and save in mongoDB

    Returns:
        str: "empty" if the no mri is input, "not digit" if the entered mri is
        not a numeric string
        int: 1 if the mri and mri2 entered are not the same, 0 indicates that
        the information entered above are successfully added

    """
    if mri == "":
        return "empty"
    if mri.isdigit() is not True:
        return "not digit"
    if mri != mri2:
        return 1
    else:
        dict_in["MRI"] = mri
        dict_in["patient_name"] = name
        return 0


# This function and it's exceptions won't be tested. This function is nothing
# but a post request to the server and the exceptions are handling situations
# like The offline situation and connection problems of the server.
# The return value
# depends on the status of the server(for example online or not which is
# unsure)
def uploader(dict_in):
    """Post the global dictionary to the server

    This function contains a post request to the flask server. The global
    dictionary in the patient GUI that saved all the information to be upload
    will be posted. This function will also catch the exceptions that the
    server can not be found or breakdown.

    Args:
        dict_in (dict): The global dictionary in the client_gui that store all
        the information to be sent to the server and save in mongoDB

    Returns:
        str: "uploaded" if the request is successfully made and "failed" if
        there are something wrong with the connection to the server

    """
    try:
        r = requests.post("http://127.0.0.1:5000/api/upload", json=dict_in)
        print(r.status_code)
        print(r.text)
        return "Uploaded"
    except (requests.exceptions.ConnectionError, ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError):
        return "failed"


def create_warehouse():
    """Create the global dictionary

    This function will create a global dictionary in the Patient GUI that
    store all the input and processed result temporarily before sending them
    to the server and store them in the mongoDB.
    The keys of the dictionary includes: patient_name which is the patient's
    name; MRI: medical record number; medical_image: medical image from the
    patient's client end; medical_title:user defined title of the medical image
    ; medical_des: user defined description of the medical image; heart_rate:
    heart rate in bps unit processed by the ecg_analysis file; ecg_image:
    cg_image generated; ecg_title: users defined title for the ecg image;
    ecg_des: users defined description of the ecg trace image.

    Returns:
        dict: The created dictionary

    """
    inform_warehouse = dict()
    inform_warehouse["patient_name"] = ""
    inform_warehouse["MRI"] = "0"
    inform_warehouse["medical_image"] = ""
    inform_warehouse["medical_title"] = ""
    inform_warehouse["medical_des"] = ""
    inform_warehouse["heart_rate"] = "0"
    inform_warehouse["ecg_image"] = ""
    inform_warehouse["ecg_title"] = ""
    inform_warehouse["ecg_des"] = ""
    return inform_warehouse
