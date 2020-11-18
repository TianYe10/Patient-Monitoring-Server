import tkinter as tk             # Import base tkinter module
from tkinter import ttk         # Import update widget module
from tkinter import filedialog   # Import module for open/save file windows

from client_MS import medical_record_number_list, \
    display_selected_patient_info, \
    save_b64_string_to_file, ECG_trace_list, display_another_ECG_image, \
    medical_image_list, display_medical_image

from PIL import Image, ImageTk   # Import Pillow to open and display JPG images


def design_window():
    """ Creates and runs main GUI window

    This function is the main portion of GUI code. Under it, many sub
    functions are added to perform different functionalities. It literally
    works as a 'window' for designing.

    Args:
        None

    Returns；
        None
    """

    periodically_request_time = 30000
    # unit:ms

    def ok_btn_cmd():
        """ Function to run when "Ok" button is clicked.

        For this GUI specifically, the command of clicking 'Ok/reload'
        button includes lots of stuff, such as clearing existing pictures,
        get the choice of MRI number selection, calling periodic
        request, etc. This function  integrates all steps that need to
        be done  whenever the user click 'ok' button on GUI in
        a preset order.

        Args:
            None

        Returns:
            None
        """

        new_ECG_trace_btn.grid_forget()
        display_another_ecg_btn.grid_forget()
        download_img_btn.grid_forget()
        choose_medical_image_btn.grid_forget()
        display_medical_image_btn.grid_forget()
        download_medical_img_btn.grid_forget()

        ECG_traces_combo.grid_forget()
        medical_images_combo.grid_forget()

        image_label1.grid_forget()
        image_label2.grid_forget()
        image_label3.grid_forget()

        status_label2.grid_forget()
        status_label3.grid_forget()
        status_label4.grid_forget()
        status_label5.grid_forget()
        status_label6.grid_forget()
        status_label7.grid_forget()
        status_label8.grid_forget()
        status_label9.grid_forget()
        status_label10.grid_forget()
        status_label11.grid_forget()
        status_label12.grid_forget()
        status_label13.grid_forget()
        status_label14.grid_forget()
        status_label15.grid_forget()
        status_label16.grid_forget()

        global MRI_output
        global list_of_ECG_traces
        MRI_output = MRI.get()
        list_of_ECG_traces = ECG_trace_list(MRI_output)
        global number, name, latest_hr, latest_ECG_image, uploaded_time
        number, name, latest_hr, latest_ECG_image, uploaded_time = \
            display_selected_patient_info(MRI_output)
        status_label5.configure(text=number + "\n" + name + "\n" + latest_hr +
                                "\n" + uploaded_time + "\n")
        status_label5.grid(column=2, row=4)

        if latest_ECG_image != "":
            save_b64_string_to_file(latest_ECG_image, "latest_ECG_image.jpg")
            pil_image = Image.open("latest_ECG_image.jpg")
            resized_image = pil_image.resize((384, 384))
            tk_image = ImageTk.PhotoImage(resized_image)
            image_label1.configure(image=tk_image)  # Change image in label
            image_label1.image = tk_image  # Stores image data as part of the
            image_label1.grid(column=2, row=7)

            status_label4.configure(text="\nThe latest ECG trace image "
                                         "is shown below",
                                    background='green')
            status_label4.grid(column=2, row=6)
        else:
            status_label3.configure(text="No available ECG trace image "
                                         "for this patient.",
                                    background='red')
            status_label3.grid(column=2, row=6)

        global list_of_medical_images
        list_of_medical_images = medical_image_list(MRI_output)
        medical_images_combo.set(list_of_medical_images[0])
        medical_images_combo['values'] = (list_of_medical_images[0:])
        medical_images_combo.state(['readonly'])
    # def ok_btn_cmd_reschedule():
    #     root.after(periodically_request_time, ok_btn_cmd)

        # Other ECG trace list entry

        new_ECG_trace_btn.grid(column=3, row=3)
        choose_medical_image_btn.grid(column=4, row=3)

        reload_latest_info()  # to make periodic request every 30s
        reload_other_images()
        reload_medical_image()

    def reload_latest_info():
        """ Function for periodic request latest patient information
        when 'Ok/reload'  button is clicked

        To meet the specification of calling the server and updating
        latest info/images every certain time(30s), this function is
        designed to take the steps which were in the ok_btn_cmd(),
        but actually runs only after 30 seconds.

        Args:
            None

        Returns:
            None
        """
        global MRI_output
        global number, name, latest_hr, latest_ECG_image, uploaded_time
        a, b, c, d, e = display_selected_patient_info(MRI_output)
        if (number, name, latest_hr, latest_ECG_image, uploaded_time) != (a, b,
                                                                          c, d,
                                                                          e):
            number = a
            name = b
            latest_hr = c
            uploaded_time = e
            status_label5.configure(text=number + "\n" + name + "\n" +
                                    latest_hr + "\n" + uploaded_time +
                                    "\n")
            status_label5.grid(column=2, row=4)
            status_label4.configure(text="\nUPDATE: THE Patient's info/ latest"
                                         "ECG record got a change!",
                                    background='green')
            status_label4.grid(column=2, row=6)
        if latest_ECG_image != d:
            if d == "":
                latest_ECG_image = d
                image_label1.grid_forget()
                status_label14.configure(text="\n No ECG trace image "
                                              "is available now.",
                                         background='red')
                status_label14.grid(column=2, row=6)
                status_label4.grid_forget()
                status_label15.grid_forget()
            else:
                latest_ECG_image = d
                save_b64_string_to_file(latest_ECG_image,
                                        "latest_ECG_image.jpg")
                pil_image = Image.open("latest_ECG_image.jpg")
                resized_image = pil_image.resize((384, 384))
                tk_image = ImageTk.PhotoImage(resized_image)
                image_label1.configure(image=tk_image)
                # Change image in label
                image_label1.image = tk_image
                # Stores image data as part of the
                image_label1.grid(column=2, row=7)
                status_label3.grid_forget()
                status_label4.grid_forget()
                status_label15.configure(text="\nUPDATED THE LATEST"
                                              " ECG TRACE IMAGE!",
                                         background='green')
                status_label15.grid(column=2, row=6)

        root.after(periodically_request_time, reload_latest_info)

    def reload_other_images():
        """ Function for periodically request new ECG images
        when 'Ok/reload'  button is clicked

        Similarly to reload_latest_info(), to meet the
        specification of indicating any update in the patient's
        ECG trace images history, this function is
        designed to take the steps which were in the ok_btn_cmd(),
        but actually runs only after 30 seconds. It shows any
        change happened in the 'ECG_record' in the database.

        Args:
            None

        Returns:
            None
        """
        global list_of_ECG_traces
        global MRI_output
        f = ECG_trace_list(MRI_output)
        if list_of_ECG_traces != f:
            list_of_ECG_traces = f
            ECG_traces_combo.set(list_of_ECG_traces[0])
            ECG_traces_combo['values'] = (list_of_ECG_traces[0:])
            ECG_traces_combo.state(['readonly'])
            if f == ['']:
                status_label6.grid_forget()
                status_label7.grid_forget()
                status_label11.grid_forget()
                status_label13.grid_forget()
                status_label2.configure(text="UPDATE: No other ECG "
                                             "images now!",
                                        background='red')
                status_label2.grid(column=3, row=4)
                display_another_ecg_btn.grid_forget()
                ECG_traces_combo.grid_forget()
                download_img_btn.grid_forget()
                image_label2.grid_forget()
            else:
                status_label2.grid_forget()
                status_label7.configure(text="Update: The list of 'other "
                                             "ECG images'\n just got a"
                                             " modification", font=my_font2)
                status_label7.grid(column=3, row=1)
                new_ECG_trace_btn.grid(column=3, row=3)
                display_another_ecg_btn.grid_forget()
                ECG_traces_combo.grid_forget()

        root.after(periodically_request_time, reload_other_images)

    def reload_medical_image():
        """ Function for periodically request new medical images
        when 'Ok/reload'  button is clicked

        Similarly to reload_latest_info(), to meet the
        specification of indicating any update in the patient's
        medical images update, this function is designed to
        take the steps which were in the ok_btn_cmd(),
        but actually runs only after 30 seconds. It shows any
        change happened in the 'medical_images' in the database.

        Args:
            None

        Returns:
            None
        """
        global list_of_medical_images
        global MRI_output
        new_list = medical_image_list(MRI_output)
        if list_of_medical_images != new_list:
            list_of_medical_images = new_list
            medical_images_combo.set(list_of_medical_images[0])
            medical_images_combo['values'] = (list_of_medical_images[0:])
            medical_images_combo.state(['readonly'])
            if new_list == ['']:
                status_label9.grid_forget()
                status_label10.grid_forget()
                status_label11.grid_forget()
                status_label13.grid_forget()
                status_label8.configure(text="UPDATE: No medical "
                                             "images now!",
                                        background='red')
                status_label8.grid(column=4, row=4)
                display_medical_image_btn.grid_forget()
                medical_images_combo.grid_forget()
                # download_medical_img_btn.grid_forget()
                # image_label3.grid_forget()
            else:
                # status_label10.grid_forget()
                status_label9.configure(text="Update: The list of medical"
                                             " images\n just got a"
                                             " modification", font=my_font2)
                status_label9.grid(column=4, row=1)
                status_label8.grid_forget()
                choose_medical_image_btn.grid(column=4, row=3)
                display_medical_image_btn.grid_forget()
                medical_images_combo.grid_forget()
        root.after(periodically_request_time, reload_medical_image)

    def cancel_btn_cmd():
        """ Closes window when Cancel is clicked.

        During the users are using GUI, whenever they want they
        should be free to click 'Cancel' at the bottom right to
        quit the GUI. It has same effect as the 'X' button on
        top right.

        Args:
            None

        Returns:
            None
        """

        root.destroy()

    #  Define font for use in display
    my_font = ("arial", 18)
    my_font2 = ("Times", 12)

    # Create root window
    root = tk.Tk()
    root.title("Monitoring-Station GUI")
    # root.geometry("800x800+400+200") # this is for windows10, this try is bad

    MRI_output = ''
    another_ecg_img = ''
    global list_of_ECG_traces
    list_of_ECG_traces = [""]
    list_of_medical_images = [""]

    # Top label in GUI
    top_label = ttk.Label(root, text="Monitoring-Station",
                          font=("arial", 18))
    top_label.grid(column=0, row=0, columnspan=2)

    instruction_label1 = ttk.Label(root, text="Select a MRI to start...",
                                   font=("Times", 10))
    instruction_label1.grid(column=0, row=1, sticky='w')
    instruction_label2 = ttk.Label(root, text="To quit, click 'Cancel'.",
                                   font=("Times", 10))
    instruction_label2.grid(column=0, row=2, sticky='w')

    # MRI number list entry
    ttk.Label(root, text="Select A Medical Record Number", font=("arial", 14))\
        .grid(column=2, row=0)

    # Style definition for ttk widgets
    update_ttk_button_style = ttk.Style()
    update_ttk_button_style.configure('BloodDonor.TButton', font=my_font)

    # Ok / Cancel Buttons
    ok_btn = ttk.Button(root, text="Ok/Reload", command=ok_btn_cmd,
                        style='Kim.TButton')
    ok_btn.grid(column=2, row=3, sticky='nw')

    cancel_btn = ttk.Button(root, text="Cancel", command=cancel_btn_cmd,
                            style='BloodDonor.TButton')
    cancel_btn.grid(column=4, row=11, sticky='e')

    # Status Label
    status_label1 = ttk.Label(root, text="Please select an available"
                                         " patient's medical record number "
                                         "from the database\nand click "
                                         'Ok/Reload'   " button "
                                         "to display", font=my_font2)
    status_label1.grid(column=2, row=1)
    status_label2 = ttk.Label(root)
    status_label3 = ttk.Label(root)
    status_label4 = ttk.Label(root)
    status_label5 = ttk.Label(root)
    status_label6 = ttk.Label(root)
    status_label7 = ttk.Label(root)
    status_label8 = ttk.Label(root)
    status_label9 = ttk.Label(root)
    status_label10 = ttk.Label(root)
    status_label11 = ttk.Label(root)
    status_label12 = ttk.Label(root)
    status_label13 = ttk.Label(root)
    status_label14 = ttk.Label(root)
    status_label15 = ttk.Label(root)
    status_label16 = ttk.Label(root)

    image_label1 = ttk.Label(root)
    image_label2 = ttk.Label(root)
    image_label3 = ttk.Label(root)

    MRI = tk.StringVar()
    MRI_combo = ttk.Combobox(root, textvariable=MRI)
    MRI_combo.grid(column=2, row=2)
    list_of_MRI = medical_record_number_list()
    list_of_MRI.sort()
    if len(list_of_MRI) == 0:
        MRI_combo.set("No patient in database now")
        ok_btn.grid_forget()
        status_label12.configure(text="Please close GUI and retry "
                                      "when a patient is "
                                      "uploaded to database.")
        status_label12.grid(column=2, row=4)
    else:
        MRI_combo.set(list_of_MRI[0])  # default value
        MRI_combo['values'] = (list_of_MRI[0:])
        MRI_combo.state(['readonly'])

    ECG_traces = tk.StringVar()
    ECG_traces_combo = ttk.Combobox(root, textvariable=ECG_traces)
    ECG_traces_combo.grid(column=3, row=3)
    ECG_traces_combo.grid_forget()
    ECG_traces_combo['values'] = (list_of_ECG_traces[0:])
    ECG_traces_combo.state(['readonly'])

    medical_images = tk.StringVar()
    medical_images_combo = ttk.Combobox(root, textvariable=medical_images)
    medical_images_combo.grid(column=4, row=3)
    medical_images_combo.grid_forget()
    medical_images_combo['values'] = (list_of_medical_images[0:])
    medical_images_combo.state(['readonly'])

    def another_ecg_img_cmd():
        """ Function for letting users choose another ECG image
        available

        This function work as the command for the button 'choose
        another ECG image'. If another ECG image exists it lets
        users to take further steps to select; if actually there
        are no any more ECG image for this patient it will show
        a string to tell users about that.

        Args:
            None

        Returns:
            None
        """
        global list_of_ECG_traces
        global MRI_output
        list_of_ECG_traces = ECG_trace_list(MRI_output)
        ECG_traces_combo.set(list_of_ECG_traces[0])
        ECG_traces_combo['values'] = (list_of_ECG_traces[0:])
        ECG_traces_combo.state(['readonly'])

        if list_of_ECG_traces == ['']:
            status_label2.configure(text="No other ECG trace images \n"
                                         "for this patient", background='red')
            status_label2.grid(column=3, row=4)
        else:
            status_label7.configure(text="Select another ECG trace\n by "
                                         "their timestamp below",
                                    font=my_font2)
            status_label7.grid(column=3, row=1)
            display_another_ecg_btn.grid(column=3, row=4)
            new_ECG_trace_btn.grid_forget()
            ECG_traces_combo.grid(column=3, row=2)
            status_label11.configure(text='All images are displayed in '
                                          '\nthe size of 256x256 on GUI,'
                                          'but \n you are able to download '
                                          '\nthe original image')
            status_label11.grid(column=0, row=4, sticky='w')
            status_label13.configure(text="Patient's all info refreshes\n"
                                          "every 30s for any update...")
            status_label13.grid(column=0, row=5, sticky='w')

    new_ECG_trace_btn = ttk.Button(root, text="Choose another ECG trace "
                                              "image",
                                   command=another_ecg_img_cmd)
    new_ECG_trace_btn.grid(column=3, row=4)
    new_ECG_trace_btn.grid_forget()

    def display_another_ecg_cmd():
        """ Function for displaying selected another ECG image

        Only when users click 'choose another ECG trace image',
        and another ECG image does exist, this button then will
        show up to let the user be able to display a selected
        ECG image on GUI.

        Args:
            None

        Returns:
            None
        """
        global another_ecg_img
        timestamp = ECG_traces.get()
        global MRI_output
        another_ecg_img = display_another_ECG_image(MRI_output,
                                                    eval(timestamp))
        save_b64_string_to_file(another_ecg_img, "another_ecg_img.jpg")
        pil_image = Image.open("another_ecg_img.jpg")
        resized_image = pil_image.resize((384, 384))
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label2.configure(image=tk_image)  # Change image in label
        image_label2.image = tk_image
        image_label2.grid(column=3, row=7)

        status_label6.configure(text="\nECG trace at {}".format(timestamp),
                                background='green')
        status_label6.grid(column=3, row=6)
        download_img_btn.grid(column=3, row=8, sticky='w')

    display_another_ecg_btn = ttk.Button(root, text="Display",
                                         command=display_another_ecg_cmd)
    display_another_ecg_btn.grid(column=3, row=5)
    display_another_ecg_btn.grid_forget()

    def download_cmd():
        """When the button is clicked, call outside function to
           make request to server to download image from server.

        Only when users click 'display' to see another ECG image,
        this button then will show up to let the user be able to
        download the image they see in a .jpg document to their
        local computer. it's a functionality for options.

        Args:
            None

        Returns:
            None
        """
        filename = filedialog.asksaveasfilename(confirmoverwrite=False,
                                                defaultextension=".jpg",
                                                filetypes=(("JPG file",
                                                            "*.jpg"),
                                                           ("All Files",
                                                            "*.*")))
        if filename == "":
            return
        global another_ecg_img
        save_b64_string_to_file(another_ecg_img, filename)

    download_img_btn = ttk.Button(root, text='Download this ECG trace image',
                                  command=download_cmd)
    download_img_btn.grid(column=3, row=8, sticky='w')
    download_img_btn.grid_forget()

    def choose_medical_image_cmd():
        """ Function for letting users choose an available
        medical image

        Similar to another_ecg_img_cmd(), this function work as
        the command for the button 'choose a medical image'.
        If a medical image exists it lets users to take further
        steps to select in a list above the button; if actually
        there are no any medical image for this patient it will
        display a string below to tell users about that.

        Args:
            None

        Returns:
            None
        """
        global MRI_output
        global list_of_medical_images
        list_of_medical_images = medical_image_list(MRI_output)
        medical_images_combo.set(list_of_medical_images[0])
        medical_images_combo['values'] = (list_of_medical_images[0:])
        medical_images_combo.state(['readonly'])

        if list_of_medical_images == ['']:
            status_label8.configure(text='Does not have any \nmedical image '
                                         'for this patient',
                                    background='red')
            status_label8.grid(column=4, row=4)
        else:
            status_label9.configure(text="Select a medical image"
                                         "\n in the list below",
                                    font=my_font2)
            status_label9.grid(column=4, row=1)
            medical_images_combo.grid(column=4, row=2)
            display_medical_image_btn.grid(column=4, row=4)
            choose_medical_image_btn.grid_forget()

    choose_medical_image_btn = ttk.Button(root, text="Choose a medical image",
                                          command=choose_medical_image_cmd)
    choose_medical_image_btn.grid(column=4, row=0)
    choose_medical_image_btn.grid_forget()

    def display_medical_image_cmd():
        """ Function for displaying selected medical image

        Similar to display_another_ecg_cmd(), only when users
        click 'Choose a medical image' button,and a medical image
        does exist, this button then will show up to let the user
        be able to display a selected medical ECG image below it.

        Args:
            None

        Returns:
            None
        """
        status_label11.configure(text='All images are displayed in \nthe '
                                      'size of 256x256 on GUI,'
                                      'but \n you are able to download '
                                      '\nthe original image.')
        status_label11.grid(column=0, row=4)
        global medical_image
        medical_image_name = medical_images.get()
        global MRI_output
        medical_image = display_medical_image(MRI_output,
                                              eval(medical_image_name))
        save_b64_string_to_file(medical_image, "medical_img.jpg")
        pil_image = Image.open("medical_img.jpg")
        resized_image = pil_image.resize((384, 384))
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label3.configure(image=tk_image)  # Change image in label
        image_label3.image = tk_image
        image_label3.grid(column=4, row=7)

        status_label10.configure(text="\nmedical image: "
                                      "{}".format(medical_image_name),
                                 background='green')
        status_label10.grid(column=4, row=6)

        if medical_image != '':
            download_medical_img_btn.grid(column=4, row=8, sticky='w')

    display_medical_image_btn = ttk.Button(root, text="Display",
                                           command=display_medical_image_cmd)
    display_medical_image_btn.grid(column=4, row=5)
    display_medical_image_btn.grid_forget()

    def download_medical_image_cmd():
        """When the button is clicked, call outside function to
           make request to server to download image from server.

        Similar to download_cmd(), only when users click 'display'
        to see a medical image on GUI,  this button then will
        show up to let the user be able to  download the image they
        see in a .jpg document to their local computer. it's also a
        functionality for options.

        Args:
            None

        Returns:
            None
        """
        filename = filedialog.asksaveasfilename(confirmoverwrite=False,
                                                defaultextension=".jpg",
                                                filetypes=(("JPG file",
                                                            "*.jpg"), ("All "
                                                                       "Files",
                                                                       "*.*")))
        if filename == "":
            return
        global medical_image
        save_b64_string_to_file(medical_image, filename)

    download_medical_img_btn = ttk.Button(root, text='Download this medical'
                                                     ' image',
                                          command=download_medical_image_cmd)
    download_medical_img_btn.grid(column=4, row=9, sticky='w')
    download_medical_img_btn.grid_forget()

    root.mainloop()
    return


if __name__ == '__main__':
    print("Running...")
    design_window()
