import struct

"""
    Accepted Values:
    2
    3
    4
"""
def check_measurement_mode(point_configuration: int):
    """
        Maps the point configuration to the corresponding measurement mode code.

        Args:
            point_configuration (int): Number of electrodes (2, 3, or 4).

        Returns:
            int: Corresponding hex code for measurement mode, or -1 if invalid.
        """
    hex_map = {
        2: 0x01,
        3: 0x03,
        4: 0x02
    }
    return hex_map.get(point_configuration, -1)


"""
    Accepted Values:
    BNC Port
    Port 1
    Main Port
    Extension Port
    Extensionport
    Extension Port 2
    Extensionport2
    Port 2
    InternalMux
"""
def check_measurement_channel(measurement_channel: str):
    """
        Returns the measurement channel code for a given channel name.

        Args:
            measurement_channel (str): Name of the channel (e.g., "Main Port").

        Returns:
            int: Corresponding channel code, or -1 if not recognized.
        """
    formatted_channel = measurement_channel.strip().lower()

    measurement_channels = {
        "bnc port": 0x01,
        "port 1": 0x01,
        "main port": 0x01,
        "extension port": 0x02,
        "extensionport": 0x02,
        "extension port 2": 0x03,
        "extensionport2": 0x03,
        "port 2": 0x03,
        "internalmux": 0x03
    }

    return measurement_channels.get(formatted_channel, -1)



"""
    accepted inputs:
    - autoranging
    - ±10 mA or 10mA
    - 100 µA or 100uA
    - 1 µA or 1uA
    - 10 nA or 10nA
    - 100, 10k, 1M, 100M
"""
def check_current_range_settings(current_measurement_range: str):
    """
        Validates and returns the code for current measurement range.

        Args:
            current_measurement_range (str): Human-readable range description.

        Returns:
            int: Corresponding code, or -1 if invalid.
        """
    input_normalized = current_measurement_range.strip().lower().replace("±", "").replace(" ", "").replace("µ", "u")

    range_map = {
        "autoranging": 0x00,
        "10ma": 0x01,
        "100ua": 0x02,
        "1ua": 0x04,
        "10na": 0x06,
        "100": 0x01,
        "10k": 0x02,
        "1m": 0x04,
        "100m": 0x06
    }

    return range_map.get(input_normalized, -1)



"""
Accepted input values for voltage range:

→ ±1 V (default):
    "±1 V"
    "1V"
    "1v"
    " 1 v "
    "±1v"
    "+/-1V"
    "+ / - 1 v"

→ ±0.09 V:
    "±0.09 V"
    "0.09V"
    "0.09v"
    "+/-0.09v"
    " ± 0.09 v "

→ Autoranging:
    "autoranging"
    " Autoranging "
"""
def check_voltage_range_settings(voltage_measurement_range: str = "±1 V"):
    """
        Validates and returns the voltage measurement range code.

        Args:
            voltage_measurement_range (str): Input voltage range string.

        Returns:
            int: Corresponding code, or -1 if invalid.
        """
    input_normalized = voltage_measurement_range.strip().lower().replace("±", "").replace("+/-", "").replace(" ", "")

    range_map = {
        "autoranging": 0x00,
        "1v": 0x01,
        "0.09v": 0x02
    }

    return range_map.get(input_normalized, -1)

def float_to_bytes(value: float) -> list:
    """
        Converts a float to a list of 4 bytes in big-endian format.

        Args:
            value (float): Value to convert.

        Returns:
            list: List of 4 bytes.
        """
    return list(struct.pack(">f", value))

def check_frequency_range(start_frequency: float, end_frequency: float):
    """
        Validates frequency range and converts to byte representation.

        Args:
            start_frequency (float or str): Starting frequency.
            end_frequency (float or str): Ending frequency.

        Returns:
            tuple: Byte lists of start and end frequencies.
        """
    start_frequency = parse_frequency(start_frequency)
    end_frequency = parse_frequency(end_frequency)

    default_start_frequency = 1000.0
    default_end_frequency = 1000000.0
    min_frequency = 1.0
    max_frequency = 10000000.0

    if start_frequency >= default_end_frequency:
        print("start frequency is greater than end frequency. Using default frequency values.")
        start_frequency = default_start_frequency
        end_frequency = default_end_frequency

    if start_frequency < min_frequency:
        print("your start frequency is less than 1. Using default start frequency.")
        start_frequency = default_start_frequency

    if end_frequency > max_frequency:
        print(f"your end frequency is greater than {max_frequency}. Using default end frequency.")
        start_frequency = default_start_frequency

    return float_to_bytes(start_frequency), float_to_bytes(end_frequency)

def check_count(count: int):
    """
        Validates and returns byte representation of frequency count.

        Args:
            count (int): Desired frequency point count.

        Returns:
            list: Byte list of float count.
        """
    min_count = 1
    max_count = 1000
    default_count = 60

    if count < min_count or count > max_count:
        print(f"count is less than or equal to {min_count} and {max_count}. Taking default count.")
        count = default_count
    return list(struct.pack(">f", float(count)))

"""
    linear: 0
    logarithmic: 1
    log: 1
"""
def check_scale(scale: str):
    """
        Converts scale string to its corresponding byte code.

        Args:
            scale (str): 'linear' or 'log'/'logarithmic'.

        Returns:
            int: Byte code for scale.
        """
    scales = {
        "linear": 0x00,
        "log": 0x01,
        "logarithmic": 0x01,
        "lin": 0x01,
    }
    if scale not in scales:
        print("Invalid scale. Setting to default scale (log).")
        return scales.get("log")
    else:
        return scales.get(scale)

def check_precision(precision):
    """
        Validates and converts precision to byte representation.

        Args:
            precision (float): Measurement precision value.

        Returns:
            list: Byte list of precision.
        """
    min_precision = 0.0001
    max_precision = 1.0
    default_precision = 1.0

    if precision < min_precision or precision > max_precision:
        print(f"Precision {precision} is out of range. Using default precision.")
        precision = default_precision

    return list(struct.pack(">f", precision))

def check_amplitude(amplitude, excitation_type):
    """
        Validates and converts amplitude value to byte format.

        Args:
            amplitude (str or float): Amplitude input.
            excitation_type (str): 'voltage' or 'current'.

        Returns:
            list: Byte list of amplitude.
        """
    excitation_type = check_excitation_type(excitation_type)

    min_amp = default_amp = max_amp = 0.0

    if excitation_type == "voltage":
        min_amp = 0.0001
        max_amp = 1.0
        default_amp = 0.1
    elif excitation_type == "current":
        min_amp = 0.000001
        max_amp = 0.01
        default_amp = 0.001

    if isinstance(amplitude, str):
        amplitude = parse_amplitude(amplitude, excitation_type)

    if amplitude is None or not (min_amp <= amplitude <= max_amp):
        print("Invalid amplitude. Setting to default amplitude.")
        amplitude = default_amp

    return list(struct.pack(">f", amplitude))


def check_excitation_type(excitation_type):
    """
        Validates the excitation type.

        Args:
            excitation_type (str): Type of excitation.

        Returns:
            str: 'voltage' or 'current'. Defaults to 'voltage'.
        """
    if excitation_type not in ["voltage", "current"]:
        print(f"Invalid excitation type. Setting to default excitation type.")
        excitation_type = "voltage"

    return excitation_type


def parse_frequency(value):
    """
        Parses frequency string and converts to Hz float.

        Args:
            value (str or float): Frequency input.

        Returns:
            float: Parsed frequency in Hz.
        """
    if isinstance(value, (int, float)):
        return float(value)

    value = value.strip().lower().replace(" ", "")
    multiplier = 1

    if value.endswith("hz"):
        if value.endswith("khz"):
            multiplier = 1e3
            value = value.replace("khz", "")
        elif value.endswith("mhz"):
            multiplier = 1e6
            value = value.replace("mhz", "")
        elif value.endswith("ghz"):
            multiplier = 1e9
            value = value.replace("ghz", "")
        else:
            value = value.replace("hz", "")

    try:
        return float(value) * multiplier
    except ValueError:
        print(f"Could not parse frequency value: {value}. Using default 1000.0 Hz.")
        return 1000.0

def parse_amplitude(value, excitation_type="voltage"):
    """
        Parses amplitude string and returns a float value.

        Args:
            value (str or float): Amplitude input.
            excitation_type (str): 'voltage' or 'current'.

        Returns:
            float or None: Parsed amplitude or None if invalid.
        """
    if isinstance(value, (int, float)):
        return float(value)

    value = value.strip().lower().replace(" ", "").replace("µ", "u")
    multiplier = 1.0

    if excitation_type == "voltage":
        if value.endswith("mv"):
            multiplier = 1e-3
            value = value.replace("mv", "")
        elif value.endswith("uv"):
            multiplier = 1e-6
            value = value.replace("uv", "")
        elif value.endswith("v"):
            multiplier = 1.0
            value = value.replace("v", "")
    elif excitation_type == "current":
        if value.endswith("ma"):
            multiplier = 1e-3
            value = value.replace("ma", "")
        elif value.endswith("ua"):
            multiplier = 1e-6
            value = value.replace("ua", "")
        elif value.endswith("na"):
            multiplier = 1e-9
            value = value.replace("na", "")
        elif value.endswith("a"):
            multiplier = 1.0
            value = value.replace("a", "")

    try:
        return float(value) * multiplier
    except ValueError:
        print(f"Could not parse amplitude value: {value}. Using default.")
        return None  # handled later in check_amplitude


def check_input_spectra(spectra):
    """
        Validates and converts spectra input to integer.

        Args:
            spectra (int or str): Number of measurement repetitions.

        Returns:
            int: Validated number of spectra.
        """
    default_spectra = 20

    try:
        spectra = int(spectra)
    except (TypeError, ValueError):
        print("Spectra must be an integer. Setting to default.")
        return default_spectra

    if not (1 <= spectra <= 65535):
        print("Spectra out of valid range (1–65535). Setting to default.")
        return default_spectra

    return spectra
