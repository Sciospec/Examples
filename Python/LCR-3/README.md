# LCR-3 Measurement Interface

This Python project presents two example scripts to configure and perform a measurement with a **Sciospec LCR-3** using a USB virtual COM port. The recorded measurement data are printed into the console as well as in a ".csv"-file.

### Features

- Connect to LCR-3 via serial port
- Ask for the device ID
- Reset the current configuration of the device to default values
- Set up a measurement with the following parameters:
    - voltage excitation at 100 mV amplitude
    - enabled auto-ranging for the current measurement
    - integration time at 1 (medium)
    - 4-point measurement at the main port, at int-1 int-2 int-3 int-4, as well as at int-5 int-6 int-7 int-8 ("int": channel of the internal multiplexer)
    - resistance and quality factor as equivalent circuit model
    - excitation frequency at 1 kHz
- Start and stop automated measurements
- Read raw measurement data

### Prerequisites

- Python 3.10+
- A connected and recognized LCR-3 device (e.g., via `COM3` on Windows as implemented in the scripts)
- Required Python packages:
  - `serial`
  - `numpy`
  - `csv`
  - `pathlib`

## Protocol Support
This project uses the official LCR-3 command set as described in the chapter "Standard Commands for Programmable Instruments (SCPI)" of the associated manual.

## Notes
Compensation was left out.


## Author
Dr. Tobias Thalheim, Sciospec Scientific Instruments GmbH

Contact: t.thalheim@sciospec.de
