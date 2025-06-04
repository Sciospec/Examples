import struct
import serial
import serial.tools.list_ports
import csv
import check_User_Input as input_user
import time


MSG_DICT = {
    "0x01": "No message inside the message buffer",
    "0x02": "Timeout: Communication-timeout (less data than expected)",
    "0x04": "Wake-Up Message: System boot ready",
    "0x11": "TCP-Socket: Valid TCP client-socket connection",
    "0x81": "Not-Acknowledge: Command has not been executed",
    "0x82": "Not-Acknowledge: Command could not be recognized",
    "0x83": "Command-Acknowledge: Command has been executed successfully",
    "0x84": "System-Ready Message: System is operational and ready to receive data",
    "0x92": "Data holdup: Measurement data could not be sent via the master interface",
}

class ISX3:

    def __init__(self) -> None:
        """
                    Initializes an ISX3 device handler.
        """
        self.serial_protocol = None
        self.device = None
        self.frequency_points = 0
        self.ret_hex_int = None
        self.print_msg = True

    def is_port_available(self, port: str) -> bool:
        """
        Checks if the specified COM port is available.

        Args:
            port (str): COM port identifier (e.g., "COM3").

        Returns:
            bool: True if the port is available, False otherwise.
        """
        available_ports = [p.device for p in serial.tools.list_ports.comports()]
        return port in available_ports

    def connect_device_fs(self, port: str):
        """
        Connects to the ISX3 device via the specified serial port (USB full-speed).

        Args:
            port (str): COM port to connect to (e.g., "COM3").

        Raises:
            serial.SerialException: If the connection cannot be established.
        """
        if not self.is_port_available(port):
            print(f"Error: Port {port} is not available.")
            return

        if hasattr(self, "serial_protocol"):
            print(
                f"Serial connection 'self.serial_protocol' already defined as {self.serial_protocol}."
            )
        else:
            self.serial_protocol = "FS"

        try:
            self.device = serial.Serial(
                port=port,
                baudrate=9600,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
            )
            print(f"Successfully Connected to {self.device.name}. \n")
        except serial.SerialException as e:
            print("Error: ", e)

    def system_message_callback_usb_fs(self):
        """
        Reads system messages from the serial buffer and interprets them.

        Returns:
            list or tuple or None: Depending on `ret_hex_int`, returns hexadecimal, integer values, both, or None.
        """
        timeout_count = 0
        received = []
        data_count = 0

        while True:
            buffer = self.device.read()
            if buffer:
                received.extend(buffer)
                data_count += len(buffer)
                timeout_count = 0
                continue
            timeout_count += 1
            if timeout_count >= 1:
                # Break if we haven't received any data
                break

            received = "".join(str(received))  # If you need all the data
        received_hex = [hex(receive) for receive in received]
        try:
            msg_idx = received_hex.index("0x18")
            if self.print_msg:
                print(MSG_DICT[received_hex[msg_idx + 2]])
        except BaseException:
            if self.print_msg:
                print(MSG_DICT["0x01"])
            # self.print_msg = False
        if self.print_msg:
            print("message buffer:\n", received_hex)
            print("message length:\t", data_count)

        if self.ret_hex_int is None:
            return None
        elif self.ret_hex_int == "hex":
            return received_hex
        elif self.ret_hex_int == "int":
            return received
        elif self.ret_hex_int == "both":
            return received, received_hex
        return None

    def write_command_string(self, command):
        """
                Writes a command to the device and processes the resulting system message.

                Args:
                    command (bytearray): Formatted command frame.
                """
        self.device.write(command)
        self.system_message_callback_usb_fs()

    def set_fs_settings(self, measurement_mode, measurement_channel="Main Port",
                        current_measurement_range="autoranging", voltage_measurement_range="1V"):
        """
                Configures the frontend settings for the measurement.

                Args:
                    measurement_mode (int): Measurement mode (1=2-point, 2=4-point, 3=3-point).
                    measurement_channel (str): Measurement channel to use (e.g., "Main Port").
                    current_measurement_range (str): Current measurement range (e.g., "10mA").
                    voltage_measurement_range (str): Voltage measurement range (e.g., "1V").

                Returns:
                    None
                """
        # Clear stack to avoid overflow
        self.write_command_string(bytearray([0xB0, 0x03, 0xFF, 0xFF, 0xFF, 0xB0]))

        # Convert parameters
        mode = input_user.check_measurement_mode(measurement_mode)
        if mode == -1:
            print(f"Invalid Measurement Mode '{measurement_mode}', set it to default Value (4 Points).")
            mode = 0x02
        current_range = input_user.check_current_range_settings(current_measurement_range)
        if current_range == -1:
            print(f"Invalid range mode '{current_measurement_range}', set it to 'autoranging'.")
            current_range = 0x00
        voltage_range = input_user.check_voltage_range_settings(voltage_measurement_range)
        if voltage_range == -1:
            print(f"Invalid voltage range '{voltage_measurement_range}', set it to ±1V.")
            voltage_range = 0x01
        channel_code = input_user.check_measurement_channel(measurement_channel)
        if channel_code == -1:
            print(f"Invalid Channel '{measurement_channel}', set it to 'Main Port'.")
            channel_code = 0x01

        # 2-byte extension channels (default to 0x0000 if not used)
        ext = [0x00, 0x00]

        # Build command based on measurement mode
        if mode == 0x01:  # 2-point
            command = [
                0xB0, 0x09, mode, current_range, voltage_range,
                channel_code, *ext,  # C channel
                channel_code, *ext,  # W channel
                0xB0
            ]
        elif mode == 0x03:  # 3-point
            command = [
                0xB0, 0x0C, mode, current_range, voltage_range,
                channel_code, *ext,  # C channel
                channel_code, *ext,  # R channel
                channel_code, *ext,  # W channel
                0xB0
            ]
        elif mode == 0x02:  # 4-point
            command = [
                0xB0, 0x0F, mode, current_range, voltage_range,
                channel_code, *ext,  # C channel
                channel_code, *ext,  # R channel
                channel_code, *ext,  # S channel
                channel_code, *ext,  # W channel
                0xB0
            ]
        else:
            print("Unsupported measurement mode. Aborting.")
            return

        self.device.write(bytearray(command))
        response = self.device.read(4)
        print("Response from device: ", response)
        print("FS settings applied.\n")

    def get_fs_settings(self):
        self.device.reset_input_buffer()

        # Step 1: Query number of configured channels
        request = bytearray([0xB1, 0x03, 0x02, 0x00, 0xB1])
        self.device.write(request)
        response = self.device.read(16)

        if len(response) < 6 or response[0] != 0xB1 or response[-1] != 0xB1:
            print("No valid B1 response frame for channel count.\n")
            return

        num_channels = int.from_bytes(response[2:4], "big")
        print(f"Number of configured channels: {num_channels}")

        if num_channels == 0:
            print("No configured frontend channels.\n")
            return

        # Step 2: Query each channel config
        for ch in range(1, num_channels + 1):
            self.device.reset_input_buffer()
            self.device.write(bytearray([0xB1, 0x02, ch, 0xB1]))
            response = self.device.read(32)

            print(f"\nRaw response for channel {ch}:", response.hex())

            for i in range(len(response)):
                if response[i] == 0xB1:
                    end_index = response.find(b'\xB1', i + 1)
                    if end_index != -1:
                        frame = response[i:end_index + 1]
                        print("Valid B1 Frame found:", frame.hex())

                        frame_type = frame[1]
                        mode = frame[2]
                        current = frame[3]
                        voltage = frame[4]

                        def get_channel_info(start_index):
                            ch = frame[start_index]
                            ext = int.from_bytes(frame[start_index + 1:start_index + 3], 'big')
                            print("\n")
                            return ch, ext

                        if frame_type == 0x09 and len(frame) == 17:  # 2-point
                            ch_c, ext_c = get_channel_info(5)
                            ch_w, ext_w = get_channel_info(8)
                            print("2-point configuration:")
                            print(f"Mode: 0x{mode:02X}, Current: 0x{current:02X}, Voltage: 0x{voltage:02X}")
                            print(f"C: 0x{ch_c:02X} (ext: {ext_c}), W: 0x{ch_w:02X} (ext: {ext_w})")

                        elif frame_type == 0x0C and len(frame) == 20:  # 3-point
                            ch_c, ext_c = get_channel_info(5)
                            ch_r, ext_r = get_channel_info(8)
                            ch_w, ext_w = get_channel_info(11)
                            print("3-point configuration:")
                            print(f"Mode: 0x{mode:02X}, Current: 0x{current:02X}, Voltage: 0x{voltage:02X}")
                            print(
                                f"C: 0x{ch_c:02X} (ext: {ext_c}), R: 0x{ch_r:02X} (ext: {ext_r}), W: 0x{ch_w:02X} (ext: {ext_w})")

                        elif frame_type == 0x0F and len(frame) == 23:  # 4-point
                            ch_c, ext_c = get_channel_info(5)
                            ch_r, ext_r = get_channel_info(8)
                            ch_s, ext_s = get_channel_info(11)
                            ch_w, ext_w = get_channel_info(14)
                            print("4-point configuration:")
                            print(f"Mode: 0x{mode:02X}, Current: 0x{current:02X}, Voltage: 0x{voltage:02X}")
                            print(f"C: 0x{ch_c:02X} (ext: {ext_c}), R: 0x{ch_r:02X} (ext: {ext_r}), "
                                  f"S: 0x{ch_s:02X} (ext: {ext_s}), W: 0x{ch_w:02X} (ext: {ext_w})")
                        else:
                            print("Unknown or unsupported frame format.")
                        break
            else:
                print("No valid B1 frame found for this channel.")
        print("\n")

    def set_setup(self, start_frequency, end_frequency, count, scale, precision, amplitude, excitation_type):
        """
                Configures the measurement setup parameters such as frequency range and signal characteristics.

                Args:
                    start_frequency (str): Starting frequency, e.g., "1kHz".
                    end_frequency (str): Ending frequency, e.g., "10MHz".
                    count (int): Number of frequency points.
                    scale (str): Scale type, "log" or "linear".
                    precision (float): Measurement precision.
                    amplitude (str): Signal amplitude.
                    excitation_type (str): Type of excitation, "voltage" or "current".
                """
        self.print_msg = False
        # resets the setup
        self.device.write(bytearray([0x86, 0x01, 0x01, 0x86]))

        self.frequency_points = count

        frequency_data = input_user.check_frequency_range(start_frequency, end_frequency)[0] + input_user.check_frequency_range(start_frequency, end_frequency)[1]

        settings_formatted = [0xB6, 0x16, 0x03]

        for data in frequency_data:
            settings_formatted.append(data)

        for data in input_user.check_count(count):
            settings_formatted.append(data)

        settings_formatted.append(input_user.check_scale(scale))

        for data in input_user.check_precision(precision):
            settings_formatted.append(data)

        for data in input_user.check_amplitude(amplitude, excitation_type):
            settings_formatted.append(data)

        settings_formatted.append(0xB6)

        self.write_command_string(bytearray(settings_formatted))

        print("Set the setup. \n")

    def start_measurement(self, spectra: int = 20):
        """
                Starts a measurement process and writes results to a CSV file.

                Args:
                    spectra (int): Number of repetitions for each frequency point.

                Returns:
                    list of tuple: List containing measurement results as (Frequency ID, Real, Imaginary).
                """
        if not self.device:
            print("Device not connected.")
            return []

        spectra = input_user.check_input_spectra(spectra)
        expected_results = spectra * self.frequency_points

        print(f"Starts the measuring for {spectra} Cycles...")

        #starts the measuring
        self.device.write(bytearray([0xB8, 0x03, 0x01, 0x00, spectra, 0xB8]))

        # Reads the Data
        results = self.read_measurement_data(expected_results=expected_results, timeout=10.0)

        # Stops the measuring
        self.stop_measurement()
        self.system_message_callback_usb_fs()  # read ACK or NACK

        # Write to CSV
        with open("measurement_results.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Frequency ID", "Real Part", "Imaginary Part"])
            for row in results:
                writer.writerow(row)

        print(f"{len(results)} Measurement Results were written into measurement_results.csv.")

        self.software_reset()
        time.sleep(6)
        return results

    def read_measurement_data(self, expected_results, timeout):
        """
                Reads measurement data frames from the serial port.

                Args:
                    expected_results (int): Expected number of measurement results.

                    timeout (float): The maximum time in seconds to wait for measurement data from the device.
                    If the expected number of results is not received within this period, the method stops reading and
                    returns the data collected up to that point. This prevents indefinite blocking in case of connection
                    issues or incomplete data transmission

                Returns:
                    list of tuple: Parsed measurement data (Frequency ID, Real, Imaginary).
                """
        start = time.time()
        results = []
        buffer = []

        while time.time() - start < timeout and len(results) < expected_results:
            byte = self.device.read(1)
            if byte:
                buffer.append(byte[0])

                if len(buffer) >= 13:
                    if buffer[-13] == 0xB8 and buffer[-12] == 0x0A and buffer[-1] == 0xB8:
                        frame = buffer[-13:]
                        freq_id = int.from_bytes(frame[2:4], "big")
                        real = struct.unpack(">f", bytes(frame[4:8]))[0]
                        imag = struct.unpack(">f", bytes(frame[8:12]))[0]
                        results.append((freq_id, real, imag))
                        buffer.clear()
        return results

    def software_reset(self):
        """
                Sends a software reset command to the device.

                Returns:
                    None
                """
        self.print_msg = True
        self.write_command_string(bytearray([0xA1, 0x00, 0xA1]))
        self.print_msg = False


    def stop_measurement(self):
        """
        Stops the measurement process.
        :return: None
        """

        self.write_command_string(bytearray([0xB8, 0x01, 0x00, 0xB8]))
