import tkinter as tk
import sys
import os
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from ecg_analysis import analysis
from client import create_warehouse, add_medical_image, add_ecg_trace
from client import add_mri_name, uploader


def design_window():
    def medical_btn_cmd():
        """Medical button command

        The ttk button that will show the medical image after click

        """
        # Initialize with empty image
        medical_image_label = ttk.Label(root, image="")
        medical_image_label.grid(column=1, row=9, sticky="w")

        def show_medical_image():
            """The function to show the medical image

            Open and display the medical image choose by users. Resize the
            image to let it fit the window size.

            Returns:
                None
            """
            # Right now we only support png and jpeg image files
            global filename
            filename = filedialog.askopenfilename(initialdir="images",
                                                  title="Select Medical Image",
                                                  filetypes=(("jpeg files",
                                                              "*.jpg"),
                                                             ("png files",
                                                              "*.png")))
            if filename == "":
                return
            pil_image = Image.open(filename)
            image_size = pil_image.size
            adj_factor = 200 / image_size[1]
            pil_image = pil_image.resize((int(image_size[0] * adj_factor),
                                          int(image_size[1] * adj_factor)))
            tk_image = ImageTk.PhotoImage(pil_image)
            medical_image_label.configure(image=tk_image)
            medical_image_label.image = tk_image
            return

        # Display the medical image
        show_medical_image()

        global filename
        if filename == "":
            return

        global add_medical_btn
        add_medical_btn = ttk.Button(root, text="Add Medical Image",
                                     command=add_medical_btn_cmd)
        add_medical_btn.grid(column=3, row=9, sticky="nw")

        # orange Sign
        orange_sign3 = ttk.Label(root, text=" ",
                                 font=18, background="orange")
        orange_sign3.grid(column=2, row=9, sticky="ne")

        # title for medical image
        medical_title = ttk.Label(root, text="Medical Image",
                                  font=18, background="pink")
        medical_title.grid(column=0, row=9, sticky="ne")

        # Disable the choose medical image button
        medical_btn.state(["disabled"])

        # Medical image filename entry
        medical_filename.set("Required: Give it a file name "
                             "to upload")
        medical_filename_entry = ttk.Entry(root,
                                           textvariable=medical_filename,
                                           font=("arial", 10, "bold"),
                                           width=50)
        medical_filename_entry.grid(column=1, row=10, sticky="w")

        # Medical image description entry
        medical_des.set("Optional: Enter brief description")
        medical_description_entry = ttk.Entry(root,
                                              textvariable=medical_des,
                                              font=("arial", 10),
                                              width=50)
        medical_description_entry.grid(column=1, row=11, sticky="w")

        def re_medical_btn_cmd():
            """The button command to reselect the medical image

            This function is intended to allow the users to reselect the
            medical image if they are not satisfied with the current image.
            This function will also enable the add image button.

            Returns:
                None
            """
            medical_image_label.configure(image="")
            medical_image_label.grid(column=1, row=9, sticky="w")
            show_medical_image()
            add_medical_btn.state(["!disabled"])
            return

        # Add the button to reselect the image
        re_medical_btn = ttk.Button(root, text="Reselect Medical Image",
                                    command=re_medical_btn_cmd)
        re_medical_btn.grid(column=3, row=9, sticky="sw")

        # yellow Sign
        yellow_sign1 = ttk.Label(root, text=" ",
                                 font=18, background="yellow")
        yellow_sign1.grid(column=2, row=9, sticky="se")
        return

    def ecg_btn_cmd():
        """The function of the select an ECG file button

        This button will enable the users to choose from different ecg data
        source file, use other scripts to process it. Save the generated ecg
        trace image to local and display it in the patient side GUI

        Returns:
            None

        """
        # initial with empty image
        ecg_image_label = ttk.Label(root, image="")
        ecg_image_label.grid(column=1, row=13, sticky="w")

        def show_ecg_results():
            """ Show the result of ecg data after being processed

            This function will load the user selected ecg data and processed it
            using the ecg_analysis script. It will then show the generated ecg
            trace image and display it in the GUI, it will also show the
            detected heart rate and generate the reselect ecg button.

            Returns:
                None

            """
            # Now only support csv and exel files
            global ecg_filename
            ecg_filename = filedialog.askopenfilename(initialdir="ecg_data",
                                                      title="Select ECG Trace"
                                                            " file",
                                                      filetypes=[("csv files",
                                                                  "*.csv"),
                                                                 ("Excel"
                                                                  " files",
                                                                  ".xlsx .xls")
                                                                 ])
            if ecg_filename == "":
                return

            global heart_rate, ecg_image_name
            heart_rate, ecg_image_name = analysis(ecg_filename)
            pil_image = Image.open(ecg_image_name)
            image_size = pil_image.size
            adj_factor = 200/image_size[1]
            pil_image = pil_image.resize((int(image_size[0] * adj_factor),
                                          int(image_size[1] * adj_factor)))
            tk_image = ImageTk.PhotoImage(pil_image)
            ecg_image_label.configure(image=tk_image)
            ecg_image_label.image = tk_image

            heart_rate_label = ttk.Label(root,
                                         text="Heart Beats"
                                              " detected: {:.2f} BPM"
                                         .format(heart_rate),
                                         font=("Times New Roman", 15, "bold"),
                                         background="red",
                                         foreground="white")
            heart_rate_label.grid(column=1, columnspan=2, row=7, sticky="w")

            # Heart rate title
            heart_rate_title = ttk.Label(root, text="Heart Rate",
                                         font=18, background="pink")
            heart_rate_title.grid(column=0, row=7, sticky="ne")
            return

        # Display the result after analysis
        show_ecg_results()

        global ecg_filename
        if ecg_filename == "":
            return

        global add_ecg_btn
        add_ecg_btn = ttk.Button(root,
                                 text="Add Heart Rate\n& ECG trace image",
                                 command=add_ecg_btn_cmd)
        add_ecg_btn.grid(column=3, row=13, sticky="nw")

        # orange Sign
        orange_sign4 = ttk.Label(root, text=" ",
                                 font=30,
                                 background="orange")
        orange_sign4.grid(column=2, row=13, sticky="ne")

        # title for ecg trace
        medical_title = ttk.Label(root, text="ECG Trace",
                                  font=18, background="pink")
        medical_title.grid(column=0, row=13, sticky="ne")

        # Disable the choose select ECG file button
        ecg_btn.state(["disabled"])

        # ECG trace image filename entry
        ecg_trace_filename.set("Required: Give it a file name "
                               "to upload")
        ecg_trace_filename_entry = ttk.Entry(root,
                                             textvariable=ecg_trace_filename,
                                             font=("arial", 10, "bold"),
                                             width=50)
        ecg_trace_filename_entry.grid(column=1, row=14, sticky="w")

        # ECG trace description entry
        ecg_des.set("Optional: Enter brief description")
        ecg_description_entry = ttk.Entry(root,
                                          textvariable=ecg_des,
                                          font=("arial", 10),
                                          width=50)
        ecg_description_entry.grid(column=1, row=15, sticky="w")

        def re_ecg_btn_cmd():
            """ The button command to reselect the ecg file

            This function will enable the users to reselect the ecg files to
            process. It will also reshow the image and the processed heart rate
            .

            Returns:
                None

            """
            ecg_image_label.configure(image="")
            ecg_image_label.grid(column=1, row=13, sticky="w")
            show_ecg_results()
            add_ecg_btn.state(["!disabled"])
            return

        # Add the button to reselect the ecg trace
        re_ecg_btn = ttk.Button(root, text="Reselect ECG Trace",
                                command=re_ecg_btn_cmd)
        re_ecg_btn.grid(column=3, row=13, sticky="sw")

        # yellow Sign
        yellow_sign2 = ttk.Label(root, text=" ",
                                 font=18, background="yellow")
        yellow_sign2.grid(column=2, row=13, sticky="se")
        return

    def submit_btn_cmd():
        """This is the function that will submit all the data entered by users
        to the server

        This function will call the functions in the client.py to add the
        information to the global dictionary and send the dictionary to the
        server. According to the patient's input. It will check if the MRI
        input is correct or not. If it the input is not a digit, it will give
        the warning "not digit" with orange background. If the input is empty,
        it will give a warning with the purple background "MRI empty", if
        different MRI are entered twice, it will warn the users with a red
        background "Discrepancy!". In all these unsuccessful situations, the
        submit button will be disabled. If the inputs are correct, it will
        check if the status of the server is Ok. If something is wrong with the
        server, it will indicate that with a red sign. Otherwise, it will show
        a green sign to indicate the successful submission of information.

        Returns:
            None

        """
        warning = add_mri_name(mri.get(), mri2.get(), name.get(),
                               inform_warehouse)

        if warning == "not digit":
            mri2_label.configure(background="orange", foreground="white",
                                 text="Not Digit! ",
                                 font=("arial", 15, "italic", "bold"))
            submit_btn.state(["disabled"])
        elif warning == "empty":
            mri2_label.configure(background="purple", foreground="white",
                                 text="MRI Empty! ",
                                 font=("arial", 15, "italic", "bold"))
            submit_btn.state(["disabled"])
        elif warning == 1:
            mri2.set("Different MRI Entered!")
            mri2_label.configure(background="red", foreground="white",
                                 text="Discrepancy! ",
                                 font=("arial", 15, "italic", "bold"))
            submit_btn.state(["disabled"])
        elif warning == 0:
            mri2_label.configure(font=("Times new Roman", 18, "bold"),
                                 text="Succeed! ",
                                 foreground="white", background="green")
            status = uploader(inform_warehouse)
            if status == "failed":
                mri2_label.configure(background="red", foreground="white",
                                     text="Server Error! ",
                                     font=("arial", 15, "italic", "bold"))
                submit_btn.state(["disabled"])
                title_label.configure(text="Ops! Something wrong with "
                                           "the server!\nRestart Later! ╥﹏╥",
                                      font=("Times New Roman", 20, "bold"),
                                      foreground="red")

        if warning != 0:
            confirm_factor.set("-")
            confirm_check = ttk.Checkbutton(root, text="Confirm",
                                            variable=confirm_factor,
                                            onvalue="+",
                                            offvalue="-", command=check_cmd)
            confirm_check.grid(column=1, row=6, sticky="w")

        return

    def add_medical_btn_cmd():
        """ Add the medical image information

        This function enable the user's to add the medical image and the title
        and descriptions. After viewing the image, if they don't want to add
        the information, they can simply don't click the add medical image
        button.

        Returns:
            None

        """
        global filename
        add_medical_image(filename, inform_warehouse, medical_filename.get(),
                          medical_des.get())
        add_medical_btn.state(["disabled"])
        return

    def add_ecg_btn_cmd():
        """ Add the ecg trace information

        This function enable the user's to add the ecg trace image/heart rate
        and the title and descriptions. After viewing the image, if they don't
        want to add the information, they can simply don't click the add heart
        rate & ECG trace button


        Returns:
            None

        """
        add_ecg_trace(ecg_image_name, heart_rate, inform_warehouse,
                      ecg_trace_filename.get(), ecg_des.get())
        add_ecg_btn.state(["disabled"])
        return

    def cancel_btn_cmd():
        """Shut down the program

        This function will destroy the root window and kill the thread of this
        running GUI.

        Returns:
            None

        """
        root.destroy()

    def check_cmd():
        """Enable or disable the submit button

        This function is designed for the check box. If the check box is
        selected it will enable the submit button that might be locked in
        the previous operations. If the check box is unselected, then the
        submit button will be locked again

        Returns:
            None
        """
        if confirm_factor.get() == "+":
            submit_btn.state(["!disabled"])
        else:
            confirm_factor.set("-")
            submit_btn.state(["disabled"])

    def clock():
        """ The clock of the GUI

        This function will generate a clock for the patient side GUI

        Returns:
            None

        """
        from time import strftime
        string = strftime('%H:%M:%S %p')
        clock_label.config(text=string)
        clock_label.after(1000, clock)

    # Generate the root window
    root = tk.Tk()
    # The title of the GUI window
    root.title("Patient-side Graphical User Interface")
    # Set the size and the initial location of the window
    # root.geometry("800x800+200+5")
    # Set the window's width can't be resized
    root.resizable(0, 1)

    # Medical File Name initial
    filename = ""

    # ECG File name initial
    ecg_filename = ""

    # Design the title of the GUI
    title_label = ttk.Label(root, text="Patient-side User Interface",
                            font=("Times New Roman", 20, "bold", "italic"))
    title_label.grid(column=1, row=0, columnspan=2, sticky="n")

    # Set the row 1 to be a blank row
    blank_row1 = ttk.Label(root, text="",
                           font=18)
    blank_row1.grid(column=0, row=1)

    # Set the row 3 to be a blank row
    blank_row3 = ttk.Label(root, text="",
                           font=10)
    blank_row3.grid(column=0, row=3)

    # Set the row 12 to be a blank row
    blank_row3 = ttk.Label(root, text="",
                           font=10)
    blank_row3.grid(column=0, row=12)

    # Set the row 16 to be a blank row
    blank_row3 = ttk.Label(root, text="",
                           font=10)
    blank_row3.grid(column=0, row=16)

    # Set the column 3 to be a blank col
    blank_col3 = ttk.Label(root, text="             ",
                           font=30)
    blank_col3.grid(column=2, row=2)

    # Design the entry to enter a patient name
    name_label = ttk.Label(root, text="Patient Name: ",
                           font=("Times new Roman", 18), foreground="blue")
    name_label.grid(column=0, row=2, sticky="e")

    name = tk.StringVar()
    name.set("Enter your full name")
    name_entry = ttk.Entry(root, textvariable=name,
                           font=("arial", 15, "italic"), width=30)
    name_entry.grid(column=1, row=2, sticky="w")

    # Design the entry to enter a MRI
    mri_label = ttk.Label(root, text="MRI: ",
                          font=("Times new Roman", 18), foreground="blue")
    mri_label.grid(column=0, row=4, sticky="e")

    mri = tk.StringVar()
    mri.set("Enter your medical record number")
    mri_entry = ttk.Entry(root, textvariable=mri,
                          font=("arial", 15, "italic"), width=30)
    mri_entry.grid(column=1, row=4, sticky="w")

    # Design the entry to re-enter a MRI
    mri2_label = ttk.Label(root, text="Re-Enter MRI: ",
                           font=("Times new Roman", 18), foreground="purple")
    mri2_label.grid(column=0, row=5, sticky="e")

    mri2 = tk.StringVar()
    mri2.set("Please Enter MRI again")
    mri2_entry = ttk.Entry(root, textvariable=mri2,
                           font=("arial", 15, "italic"), width=30)
    mri2_entry.grid(column=1, row=5, sticky="w")

    # The button to show and display the medical image
    medical_btn = ttk.Button(root, text="Choose Medical Image",
                             command=medical_btn_cmd)
    medical_btn.grid(column=3, row=2, sticky="e")

    # orange Sign
    orange_sign1 = ttk.Label(root, text=" ",
                             font=18, background="orange")
    orange_sign1.grid(column=2, row=3, sticky="e")

    # The button to select and process the ECG files
    ecg_btn = ttk.Button(root, text="     Select an ECG file     ",
                         command=ecg_btn_cmd)
    ecg_btn.grid(column=3, row=3, sticky="e")

    # orange Sign
    orange_sign2 = ttk.Label(root, text=" ",
                             font=18, background="orange")
    orange_sign2.grid(column=2, row=2, sticky="e")

    # The button to submit the data
    submit_btn = ttk.Button(root, text="           SUBMIT           ",
                            command=submit_btn_cmd)
    submit_btn.grid(column=3, row=4, sticky="w")

    # Green Sign
    green_sign = ttk.Label(root, text=" ",
                           font=18, background="green")
    green_sign.grid(column=2, row=4, sticky="e")

    # Set the row 5 to be a blank row
    blank_row1 = ttk.Label(root, text="",
                           font=18)
    blank_row1.grid(column=3, row=5)

    # The button to exit the GUI
    exit_btn = ttk.Button(root, text="        EXIT        ",
                          command=cancel_btn_cmd)
    exit_btn.grid(column=3, row=6, sticky="w")

    # Red Sign
    red_sign = ttk.Label(root, text=" ",
                         font=18, background="red")
    red_sign.grid(column=2, row=6, sticky="e")

    # Set the row 7 to be a blank row
    blank_row3 = ttk.Label(root, text="",
                           font=10)
    blank_row3.grid(column=0, row=7)

    # Set the row 8 to be a blank row
    blank_row3 = ttk.Label(root, text="",
                           font=10)
    blank_row3.grid(column=0, row=8)

    # Set the medical description entry
    medical_des = tk.StringVar()

    # Set the medical image filename entry
    medical_filename = tk.StringVar()

    # Set the ecg description entry
    ecg_des = tk.StringVar()

    # Set the ecg image filename entry
    ecg_trace_filename = tk.StringVar()

    # Design the clock for the GUI
    clock_label = ttk.Label(root, font=('calibri', 15, 'bold'),
                            background='purple',
                            foreground='white')
    clock_label.grid(column=3, row=0, sticky="e")

    # Confirm the submission
    confirm_factor = tk.StringVar()

    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Run the clock
    clock()

    def help_btn_cmd():
        help_window = tk.Toplevel()
        help_window.title("? Help")
        # Set the column 0 to be a blank col
        blank_col0 = ttk.Label(help_window, text=" ",
                               font=30)
        blank_col0.grid(column=0, row=0, padx=20, pady=10)
        # Set the column 2 to be a blank col
        blank_col2 = ttk.Label(root, text=" ",
                               font=30)
        blank_col2.grid(column=2, row=1, padx=20, pady=10)

        qa_label = ttk.Label(help_window, text="Q&A",
                             font=("Times New Roman", 20, "bold", "italic"),
                             foreground="purple")
        qa_label.grid(column=1, row=1, sticky="sw")

        q1_label = ttk.Label(help_window, text="What is this?",
                             font=("arial", 15, "italic", "bold"))
        q1_label.grid(column=1, row=3, sticky="sw")

        a1_label = ttk.Label(help_window, text="This is the Patient Side GUI "
                                               "designed for the "
                                               "Patient-MonitoringStation "
                                               "Server.",
                             font=("arial", 15))
        a1_label.grid(column=1, row=4, sticky="sw")

        q2_label = ttk.Label(help_window, text="How it works?",
                             font=("arial", 15, "italic", "bold"))
        q2_label.grid(column=1, row=6, sticky="sw")

        a2_label = ttk.Label(help_window, text="Here you can choose your "
                                               "medical image, analyze your "
                                               "ecg data, and upload or \n"
                                               "update"
                                               " your medical information"
                                               " according "
                                               "to your name and MRI.",
                             font=("arial", 15))
        a2_label.grid(column=1, row=7, sticky="sw")

        qa2_label = ttk.Label(help_window, text="User Manual",
                              font=("Times New Roman", 20, "bold", "italic"))
        qa2_label.grid(column=1, row=9, sticky="sw")

        a3_label = ttk.Label(help_window, text="For detailed instructions, "
                                               "check this link -->",
                             font=("arial", 15), foreground="Blue")
        a3_label.grid(column=1, row=10, sticky="sw")
        a3_label.bind("<Button-1>", lambda e: callback("https://sites.google."
                                                       "com/view/"
                                                       "patientmonitoring"
                                                       "-station-serv/"
                                                       "patient-side-gui-"
                                                       "manual"))

        contact_label = ttk.Label(help_window, text="Leave us a Message",
                                  font=("arial", 15, "bold"),
                                  foreground="white",
                                  background="blue")
        contact_label.grid(column=1, row=12, sticky="se")
        contact_label.bind("<Button-1>",
                           lambda e:
                           callback("https://forms.gle/gei6aqDrK9ShsHuG7"))

        # Set the row 2 to be a blank row
        b_row1 = ttk.Label(help_window, text="", font=18)
        b_row1.grid(column=0, row=2)
        # Set the row 5 to be a blank row
        b_row1 = ttk.Label(help_window, text="", font=18)
        b_row1.grid(column=0, row=5)
        # Set the row 8 to be a blank row
        b_row1 = ttk.Label(help_window, text="", font=18)
        b_row1.grid(column=0, row=8)
        # Set the row 11 to be a blank row
        b_row1 = ttk.Label(help_window, text="", font=18)
        b_row1.grid(column=0, row=11)
        # Set the row 13 to be a blank row
        b_row1 = ttk.Label(help_window, text="", font=18)
        b_row1.grid(column=0, row=13)

        import webbrowser

        def callback(url):
            webbrowser.open_new(url)

    help_btn = ttk.Button(root, text="?Help", command=help_btn_cmd)
    help_btn.grid(column=3, row=16)

    # Red Sign
    red_sign2 = ttk.Label(root, text=" ",
                          font=18, background="red")
    red_sign2.grid(column=2, row=5, sticky="e")

    def restart_program():
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.
        """
        python = sys.executable
        os.execl(python, python, *sys.argv)

    restart_button = ttk.Button(root, text="   RESTART   ",
                                command=restart_program)
    restart_button.grid(column=3, row=5, sticky="w")

    inform_warehouse = create_warehouse()

    root.mainloop()
    return


if __name__ == "__main__":
    design_window()
