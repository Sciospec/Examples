from ISX3 import ISX3


try:
    isx3 = ISX3(n_el=4)
    isx3.connect_device_fs(port="COM3")  # change to com port if necessary

    isx3.set_fs_settings(
        measurement_mode=2,
        measurement_channel="Main Port",
        current_measurement_range="10mA",
        voltage_measurement_range="autoranging"
    )

    isx3.set_setup(
        start_frequency="1kHz",
        end_frequency="10MHz",
        count=10,
        scale="log",
        precision=1.0,
        amplitude="100mV",
        excitation_type="voltage"
    )

    results = isx3.start_measurement(spectra=2)

    print("Result Array: ", results)

except AttributeError:
    print("Device is not connected.")
