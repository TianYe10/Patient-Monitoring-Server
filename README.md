[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
BME 547 Final Project

### DUKE VM  
vcm-17294.vm.duke.edu  

## Patient side GUI
+ Allow the user to enter a patient name.
  + Allow the user to enter a patient medical record number.
  + Allow the user to select and display a medical image from the local 
  computer.
  + Allow the user to select an ECG data file from the local computer.  This
  ECG data should then be analyzed for heart rate in beats per minute, display 
  the resulting heart rate in the GUI, and display an image of the ECG 
  trace in the interface.
  + Upon user command, issue a RESTful API request to your server to upload
  whatever information is entered above.  The interface should only allow this
  request to be made if at least a medical record number has been entered.
  Data to upload should include the medical record number, patient name,
  measured heart rate/ECG image, and medical image.  If an item was not
  selected or added, it does not need to be uploaded.  
  + The user should have the ability to update any of this information in the
  GUI and upload the new information to the server.
  
## Patien side GUI to Server
* Accept uploads from the patient-side client that will include, at a minimum,
the medical record number.  The upload may also include a name, medical image, 
and/or heart rate & ECG image.
* Communicate with and utilize a persistent database that will store the above
uploaded data for retrieval at a future time.  
* When a heart rate and ECG image are received, the date and time of receipt 
should be stored with the data.
* If the upload contains a medical record number not already found in the 
database, a new entry should be made for that patient.  
* If the upload contains a medical record number already found in the database,
the other information sent (medical image or heart rate/ECG image) should be
added to the existing information. (For this assignment, the patient name will 
only be created the first time and does not to be updated.)
  
## Detailed User Manual
The detailed manual can be found in the wiki:  
https://github.com/BME547-Fall2020/final-project-hu-tian/wiki

## Monitoring-Station GUI

· When running pytest files for this project, it is highly recommended to keep the GUI closed when running, or it sometimes
will make an error in the get_patient_MRI_list() function test because the GUI does periodic request and influences variables.
ALSO, PLEASE DON'T RUN test_client_MS.py and test_server.py at the same time because they both require modification to database
to realize the pytest, and it will have a high chance if they modifying database at the same time. Please run pytest for them separately and 
both of them should pass as fine.


·Once you select a patient and click 'Ok', the GUI will refresh
                                          "every 30s to reload any \n info modification/addition/reduction "
                                          "for this patient.\n"
                                          "You may have to choose the another ECG trace/medical image\n "
                                          "to display them again

· The server doesn't check the data type it receives(e.g. if it gets a string of timestamp to find that ECG image).
  Than is because, the monitoring-station GUI only allows users to click, choose and submit their choices, instead of 
  any method to let users type or input any customized string. So the result the server gets must satisfies its expectations,
  or it won't give the user a chance to choose a bad input(e.g. a string for patient id number)

· During the usage of monitoring-station GUI, some temporary images will have to be downloaded/created under
  the program folder path: they are 'latest_ECG_image.jpg', 'medical_img.jpg' and 'another_ecg_img.jpg'.
  They are created due to the code in Monitoring-Station_GUI.py, if possible please just leave them there because they have no harm and provide the functionalities to
  display selected images and let users to save them locally. If you delete any of these images it may cause that
  some of the designed functionalities of GUI would not perform.
  
· In the popped window for downloading an ECG image or a medical image, the default setting is to save the image in .jpg 
  unless you specify a document type. However, you are free to choose whatever file path, or type in whatever the filename you want for the image to be saved.
  
· When running pytest files for this project, it is highly recommended to keep the GUI closed when running, or it sometimes
will make an error in the get_patient_MRI_list() function test because the GUI does periodic request and influences variables.


  ## Video demos
  ·Patient-side GUI
  <a href="https://www.loom.com/share/3f7d47fe45074097ad7c2ec49db90617"> <p>Patient GUI part1 - Watch Video</p> <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/3f7d47fe45074097ad7c2ec49db90617-with-play.gif"> </a>
  <a href="https://www.loom.com/share/5808c8be02dd42b89a9ddc687b5a30e8"> <p>Patient GUI part2 - Watch Video</p> <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/5808c8be02dd42b89a9ddc687b5a30e8-with-play.gif"> </a>
  
  ·Monitoring-station GUI:
  https://www.loom.com/share/4d6bb6ec0faa4e24ae47b466d69495f6
  
