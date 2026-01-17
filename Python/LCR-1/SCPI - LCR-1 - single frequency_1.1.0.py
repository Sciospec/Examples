# Python script that exemplifies typical steps to set up a measurement with an LCR-1 at a single frequency using the SCPI protocol.
# Author: Dr. Tobias Thalheim
# Date: 17.01.2026
# Valid from release 1.1.0 on

import serial
import pandas as pd
import csv
from pathlib import Path

# Header of the data files in dependence on the measurement type
header_in_data_file = {1: ["|Z| [Ohm]", "Theta [Degree]"],
                       2: ["Z_real [Ohm]", "Z_imag [Ohm]"],
                       3: ["L [Henry]", "Q"],
                       4: ["C [Farad]", "D"],
                       5: ["R [Ohm]", "Q"],
                       6: ["R_p [Ohm]", "C_p [Farad]"],
                       7: ["R_p [Ohm]", "L_p [Henry]"],
                       8: ["R_s [Ohm]", "C_s [Farad]"],
                       9: ["R_s [Ohm]", "L_s [Henry]"],
                       10: ["|Y| [Siemens]", "Theta [Degree]"],
                       11: ["G [Siemens]", "B [Siemens]"]
                       }

# Generating a folder that will contain the measurement data as ".csv"-files
folder_dir = Path(__file__).resolve().parent / "data"
folder_dir.mkdir(exist_ok=True)

# Open the connection to the device
COM_PORT = "COM3"  # instrument port location
TIMEOUT = 1        # [s] waiting time for time-out issues
with serial.Serial(port=COM_PORT, timeout=TIMEOUT, write_timeout=TIMEOUT,) as serial_connection:

    # Getting the device ID
    DEVICE_ID_COMMAND = "*IDN?\n"
    serial_connection.write(DEVICE_ID_COMMAND.encode())
    print("Device ID: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the ID command: " + serial_connection.readline().decode().strip())
    print("\n")

    # Resetting the instrument to default values
    RESET_COMMAND = "*RST\r\n"
    serial_connection.write(RESET_COMMAND.encode())
    print("Acknowledgement of the reset command: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the LCR measurement mode
    MODE_COMMAND = "MODE LCR\n"
    serial_connection.write(MODE_COMMAND.encode())
    print("Acknowledgement of the mode command: " + serial_connection.readline().decode().strip())
    MODE_CHECK_COMMAND = "MODE?\n"
    serial_connection.write(MODE_CHECK_COMMAND.encode())
    print("Mode: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the mode request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the excitation type to voltage
    EXCITATION_COMMAND = "LEVEL:TYPE V\n"
    serial_connection.write(EXCITATION_COMMAND.encode())
    print("Acknowledgement of the excitation command: " + serial_connection.readline().decode().strip())
    EXCITATION_CHECK_COMMAND = "LEVEL:TYPE?\n"
    serial_connection.write(EXCITATION_CHECK_COMMAND.encode())
    print("Excitation type: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the excitation type request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the excitation amplitude to 100 mV
    VOLTAGE_COMMAND = "LEVEL:VOLTAGE 0.1\n"
    serial_connection.write(VOLTAGE_COMMAND.encode())
    print("Acknowledgement of the voltage amplitude command: " + serial_connection.readline().decode().strip())
    VOLTAGE_CHECK_COMMAND = "LEVEL:VOLTAGE?\n"
    serial_connection.write(VOLTAGE_CHECK_COMMAND.encode())
    print("Voltage amplitude: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the voltage amplitude request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the associated current range to auto-ranging
    AUTORANGE_COMMAND = "FUNCTION:IMPEDANCE:RANGE:AUTO 1\n"
    serial_connection.write(AUTORANGE_COMMAND.encode())
    print("Acknowledgement of the auto-ranging command: " + serial_connection.readline().decode().strip())
    AUTORANGE_CHECK_COMMAND = "FUNCTION:IMPEDANCE:RANGE:AUTO?\n"
    serial_connection.write(AUTORANGE_CHECK_COMMAND.encode())
    print("Auto-ranging: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the auto-ranging request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the integration time to 1
    INTEGRATION_TIME_COMMAND = "APERTURE 1\n"
    serial_connection.write(INTEGRATION_TIME_COMMAND.encode())
    print("Acknowledgement of the integration time command: " + serial_connection.readline().decode().strip())
    INTEGRATION_TIME_CHECK_COMMAND = "APERTURE?\n"
    serial_connection.write(INTEGRATION_TIME_CHECK_COMMAND.encode())
    print("Integration time: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the integration time request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the measurement mode to a 4-point measurement
    MEASUREMENT_MODE_COMMAND = "FUNCTION:MEASUREMENT:MODE 4\n"
    serial_connection.write(MEASUREMENT_MODE_COMMAND.encode())
    print("Acknowledgement of the measurement mode command: " + serial_connection.readline().decode().strip())
    MEASUREMENT_MODE_CHECK_COMMAND = "FUNCTION:MEASUREMENT:MODE?\n"
    serial_connection.write(MEASUREMENT_MODE_CHECK_COMMAND.encode())
    print("Measurement mode: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the measurement mode request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Using, e.g., the capacitance model for a measurement, i.e., model 4
    model_number = 4
    MODEL_COMMAND = "FUNCTION:MEASUREMENT:TYPE " + str(model_number) + "\n"
    serial_connection.write(MODEL_COMMAND.encode())
    print("Acknowledgement of the model command: " + serial_connection.readline().decode().strip())
    MODEL_CHECK_COMMAND = "FUNCTION:MEASUREMENT:TYPE?\n"
    serial_connection.write(MODEL_CHECK_COMMAND.encode())
    print("Model: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the model request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Setting the measurement frequency to 1000 Hz
    frequency = 1000
    FREQUENCY_COMMAND = "FREQUENCY " + str(frequency) + "\n"
    serial_connection.write(FREQUENCY_COMMAND.encode())
    print("Acknowledgement of the frequency command: " + serial_connection.readline().decode().strip())
    FREQUENCY_CHECK_COMMAND = "FREQUENCY?\n"
    serial_connection.write(FREQUENCY_CHECK_COMMAND.encode())
    print("Frequency: " + serial_connection.readline().decode().strip())
    print("Acknowledgement of the frequency request: " + serial_connection.readline().decode().strip())
    print("\n")

    # Generating an empty ".csv"-file that will be filled with the measurement data
    data_file_name = str(frequency) + " Hz.csv"
    data_dir = folder_dir / data_file_name
    with open(data_dir, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header_in_data_file[model_number])

    # Start a measurement and let the system record data over 10 individual runs.
    START_COMMAND = "*TRG\n"
    serial_connection.write(START_COMMAND.encode())
    print("Acknowledgement of the start command: " + serial_connection.readline().decode().strip())
    number_of_runs = 5           # Total number of measurement runs
    run_counter = 0              # Counter for current measurement run
    # Pandas data frame storing the measurement data
    measurement_data = pd.DataFrame(columns=["first parameter", "second parameter"])
    while run_counter < number_of_runs:
        data = serial_connection.readline().decode().strip()
        # In case of unfortunate measurement settings, additionally to the measurement data, the device sends the
        # information whether an over-current or over-voltage event have been detected. In this example, this
        # information is not stored in the measurement data frame.
        if data == "Out of range: Over current detected" or data == "Out of range: Over voltage detected":
            print("Out of range detected")
            continue
        print("Measurement data: " + str(data))
        # Saving the data into the respective data file
        with open(data_dir, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([data.split(",")[0].strip(), data.split(",")[1].strip()])
        run_counter += 1

    # Stop the measurement
    STOP_COMMAND = "ABORT\n"
    serial_connection.write(STOP_COMMAND.encode())
    # As the device might have still sent some measurement data, the following lines actively search for the
    # acknowledgement as return on the ABORT command.
    acknowledgement = ""
    max_attempts = 10             # Preventing potential infinity loops

    while max_attempts > 0:
        line = serial_connection.readline().decode().strip()
        # Checking if the real line is an acknowledgment (or not-acknowledgement) command
        if line in ("OK", "NOT OK"):
            acknowledgement = line
            break

        max_attempts -= 1

    if acknowledgement:
        print("Acknowledgement of the stop command: " + acknowledgement)
    else:
        print("No valid acknowledgement line for ABORT included")