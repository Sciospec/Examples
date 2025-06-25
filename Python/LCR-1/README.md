# LCR-1 Measurement Interface

This Python project presents two example scripts to configure and perform a measurement with a **Sciospec LCR-1** using a USB virtual COM port. The recorded measurement data are printed into the console.

## Features

- Connect to LCR-1 via serial port
- Ask for the device ID
- Reset the current configuration of the device to default values
- Set up a measurement with the following parameters:
    - voltage excitation at 100 mV amplitude
    - enabled auto-ranging for the current measurement
    - integration time at 1 (medium)
    - 4-point measurement
    - capacity and dissipation factor as equivalent circuit model
    - "SCPI - LCR-1 - single frequency.py": excitation frequency at 1 kHz
    - "SCPI - LCR-1 - several frequencies.py": excitation frequencies at 1 kHz, 10 kHz, 100 kHz, 1 MHz, and 10 MHz
- Start and stop automated measurements
- Read raw measurement data

## Prerequisites

- Python 3.10+
- A connected and recognized LCR-1 device (e.g., via `COM3` on Windows as implemented in the scripts)
- Required Python packages:
  - `serial`
  - `pandas`
  - `numpy`

# Protocol Support
This project uses the official LCR-1 command set as described in the chapter "Standard Commands for Programmable Instruments (SCPI)" of the associated manual.

# Notes

- Compensation was left out

# Author
