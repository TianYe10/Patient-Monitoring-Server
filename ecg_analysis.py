def analysis(filename):
    file_name = filename

    def data_check(file_name):
        """Check if NAN exists

        Check if missing data exists in the .csv file. If exists raise an
        Exception
        and log it as an error.

        Args:
            file_name (string): The name of the file to be processed

        Returns:
            None
        """
        import numpy as np
        import math
        import sys
        try:
            data = np.genfromtxt(file_name, delimiter=",")
        except IOError:
            print("File not found!")
            sys.exit("ReEnter the file name!")
        for i in range(len(data[:, 0])):
            if math.isnan(data[i, 1]) is True or math.isnan(data[i, 0]) \
                    is True:
                ecg_logging(2, "Value Missing in {}!".format(file_name))
                raise Exception("Value not a number exists in file!")
        return

    def nan_interpolate(data):
        """Remove all the NAN values

        If NANs exist. If it is the first element, replace it with the
        value behind
        If it is the middle element, replace it with the average
        If it is the last value, replace it with the previous value

        Args:
            data (ndarray): the data you read in from csv file

        Returns:
            ndarray: The numpy ndarray without NANs
        """
        import math
        for i in range(len(data[:, 0])):
            if math.isnan(data[i, 0]) is True:
                if i == 0:
                    data[i, 0] = data[i + 1, 0]
                elif i == len(data[:, 0]) - 1:
                    data[i, 0] = data[i - 1, 0]
                else:
                    data[i, 0] = (data[i - 1, 0] + data[i + 1, 0]) / 2

        for i in range(len(data[:, 1])):
            if math.isnan(data[i, 1]) is True:
                if i == 0:
                    data[i, 1] = data[i + 1, 1]
                elif i == len(data[:, 1]) - 1:
                    data[i, 1] = data[i - 1, 1]
                else:
                    data[i, 1] = (data[i - 1, 1] + data[i + 1, 1]) / 2
        return data

    def ecg_logging(level, description):
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
        logging.basicConfig(filename="ecg_logging.log", level=logging.INFO,
                            format="%(asctime)s:%(levelname)s:%(message)s")
        if level == 0:
            logging.info(description)
        elif level == 1:
            logging.warning(description)
        elif level == 2:
            logging.error(description)
        return

    # This function won't be tested since it is only used to catch exceptions
    # And read the csv file
    def data_preprocessing(file_name):
        """The function preprocess the data

        This function call the nan_interpolate() function and simply catch the
        error raised in that function and read the csv file

        Args:
            file_name (string): The name of the csv file

        Returns:
            ndarray: The numpy array without NAN
        """
        import numpy as np
        import sys
        ecg_logging(0, "Starting analysis the ECG trace {}".format(file_name))
        try:
            data = np.genfromtxt(file_name, delimiter=",")
            processed_data = data
        except IOError:
            print("File not found!")
            ecg_logging(2, "{} does not exist".format(file_name))
            sys.exit("ReEnter the filename!")
        try:
            data_check(file_name)
        except Exception:
            processed_data = nan_interpolate(data)
            # exception logged in nan_interpolate
            print("Missing values in file!")
        return processed_data

    def butter_band_pass(data, fs, lowcut, highcut, order=5):
        """Butterworth bandpass filter

        Filter out the noise signals <1HZ or >50HZ

        Args:
            data (numpy.ndarray): signal data
            lowcut (float): lowcut frequency
            highcut (float): highcut frequency
            fs (float): system frequency
            order (int): order of the filter

        Returns:
            numpy.ndarray: clean data after filtering
        """
        from scipy.signal import butter, sosfilt
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype="band",
                     output="sos")
        filtered = sosfilt(sos, data)
        return filtered

    def ecg_peaks(data):
        """Detect the ecg peaks

        Call the signal.find_peaks to find peaks in the ECG signals.

        Args:
            data (numpy.ndarray): clean data after filtering

        Returns:
            numpy.ndarray: ECG peaks detected
        """
        import numpy as np
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(data, height=np.amax(data)/2, distance=100)
        ecg_logging(0, "ECG peaks detected")
        return peaks

    def plot_ecg(processed_data, clean_data, peaks):
        """Plot the ECG trace with found peaks

        Optional plotting function

        Args:
            processed_data (numpy.ndarray): data before filtering
            clean_data (numpy.ndarray): data after filtering
            peaks (numpy.ndarray): peaks detected

        Returns:
            None
        """
        import numpy as np
        import math
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(processed_data[:, 0], clean_data)
        plt.plot(processed_data[:, 0][peaks], clean_data[peaks], "x")
        plt.plot(np.add(np.zeros(math.ceil(processed_data[-1, 0])),
                        np.amax(clean_data) / 2), "--", color="gray")
        plt.title("ECG Peaks detected.")
        plt.xlabel("S")
        import os
        saved_name = os.path.basename(file_name)
        saved_name = os.path.splitext(saved_name)[0]
        file_string = "{}.png".format(saved_name)
        plt.savefig(file_string)
        return file_string

    def ecg_calculator(file_name, processed_data, peaks):
        """Calculate the metrics of ECG

        Calculate the metrics of ecg and generate a dict to store the
        information
        in the keys

        Args:
            file_name (string): The file name of csv file
            processed_data (numpy.ndarray): data before filtering
            peaks (numpy.ndarray): peaks detected

        Returns:
            dictionary: The dictionary contains the metrics information
        """
        # Duration of the ECG strip
        import numpy as np
        duration = processed_data[-1, 0] - processed_data[1, 0]
        ecg_logging(0, "Calculating duration :{}".format(duration))
        min, max = np.amin(processed_data[:, 1]), np.amax(processed_data[:, 1])
        if min <= -300 or max >= 300:
            ecg_logging(1, "Abnormal voltages!"
                           " file-{} max-{}, min-{}".format(file_name,
                                                            max, min))
        # Include minimum and maximum lead values
        voltage_extremes = (min, max)
        ecg_logging(0, "Calculating voltage_extremes :{}".
                    format(voltage_extremes))
        # Number of detected beats in ECG strip
        num_beats = len(peaks)
        ecg_logging(0, "Calculating num_beats :{}".format(num_beats))
        # Estimated average heart rate
        mean_hr_bpm = (num_beats / duration) * 60
        ecg_logging(0, "Calculating mean_hr_bpm :{}".format(mean_hr_bpm))
        # List of times when a beat occurred
        beats = (processed_data[:, 0][peaks]).tolist()
        ecg_logging(0, "Calculating beats :{}".format(beats))
        # Save data in keys of dictionary metrics
        metrics = {}
        metrics["duration"] = duration
        metrics["voltage_extremes"] = voltage_extremes
        metrics["num_beats"] = num_beats
        metrics["mean_hr_bpm"] = mean_hr_bpm
        metrics["beats"] = beats
        ecg_logging(0, "Metrics dictionary generated")
        return metrics

    def dict_to_json(dict_in, file_name):
        """Save dictionary into json file

        Dictionary to json

        Args:
            dict_in (dictionary): The dictionary you want ro save
            file_name (string): The original .csv file name

        Returns:
            None
        """
        import json
        with open(file_name[0:-4]+".json", "w") as write_file:
            json.dump(dict_in, write_file)
        ecg_logging(0, "Json file {} created".format(file_name[0:-4]+".json"))

    def user_output(metrics):
        """User output

        Print out all the metrics values and let users to decide if they
        need to
        plot the ECG

        Args:
            metric (dictionary): include all the metrics information

        Returns:
            string: y/n
        """
        print("The duration of ECG strip (s): " + str(metrics["duration"]))
        print("The minimum and maximum voltages (mv): " +
              str(metrics["voltage_extremes"]))
        print("The number of beats detected: " + str(metrics["num_beats"]))
        print("Average heart rate per minute: " + str(metrics["mean_hr_bpm"]))
        print("When beats occurred (s): " + str(metrics["beats"]))

    processed_data = data_preprocessing(file_name)
    # <1HZ >15HZ removed (>50hz) will also be removed
    frequency = fs = processed_data.shape[0] / processed_data[-1, 0]
    clean_data = butter_band_pass(processed_data[:, 1], frequency,
                                  lowcut=1, highcut=15)
    peaks = ecg_peaks(clean_data)
    metrics = ecg_calculator(file_name, processed_data, peaks)
    dict_to_json(metrics, file_name)
    ecg_logging(0, "Plotting enabled")
    file_string = plot_ecg(processed_data, clean_data, peaks)
    return metrics["mean_hr_bpm"], file_string


if __name__ == "__main__":
    heart_rate = analysis("ecg_data/test_data1.csv")
