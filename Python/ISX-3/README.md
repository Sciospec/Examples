# ISX-3 Measurement Interface

This Python project provides a complete interface to communicate with the **Sciospec ISX-3** impedance analyzer using a USB virtual COM port. It allows configuring the device, setting up measurement parameters, starting/stopping measurements, and exporting results to CSV format.

## Features

- Connect to ISX-3 via serial port (Full-Speed USB)
- Configure frontend settings (2-, 3-, or 4-point measurements)
- Set up custom frequency sweeps and signal amplitudes
- Start and stop automated impedance measurements
- Read and parse raw measurement data
- Export results as CSV
- Modular structure with separate validation functions

## Prerequisites

- Python 3.7+
- A connected and recognized ISX-3 device (e.g., via `COM3` on Windows)
- Required Python packages:
  - `pyserial`
  - `struct`
  - `csv`

Install dependencies using:

```bash
pip install pyserial
```


# Project Structure
```
ScioPy-ISX3/
├── .gitignore
├── README.md
└── src/
    ├── __init__.py                  # Makes src a package
    ├── ISX3.py                      # Main class to control ISX-3 device
    ├── check_User_Input.py          # Validation and parsing functions
    ├── main_script.py               # Example script to run measurements
    └── measurement_results.csv      # Output file with measurement data
```

# Example Usage
```
from src.ISX3 import ISX3

isx3 = ISX3(n_el=4)
isx3.connect_device_FS(port="COM3")

isx3.set_fs_settings(
    measurement_mode=4,
    measurement_channel="Main Port",
    current_measurement_range="10mA",
    voltage_measurement_range="autoranging"
)

isx3.set_setup(
    start_frequency="1kHz",
    end_frequency="10MHz",
    count=50,
    scale="log",
    precision=1.0,
    amplitude="100mV",
    excitation_type="voltage"
)

results = isx3.start_measurement(spectra=10)
print(results)

```

# Output
```
Frequency ID, Real Part, Imaginary Part
0, 123.45, -67.89
...
```

# Protocol Support
This project uses the official ISX-3 command set as described in the Sciospec Communication Interface documentation (e.g., commands 0xB0, 0xB6, 0xB8, etc.).

# Notes
Compensation steps (open/short/load) are not yet automated

Time-stamping and current range extensions are not enabled by default

This version assumes usage of Full-Speed USB serial mode

# Author
Quentin Kleinert
Contact: quentinkleinert850@gmail.com


