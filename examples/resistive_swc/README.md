# Description

This directory contains an example of interfacing resistive steering wheel controls (based on a resistor ladder) with the Hudiy API.

The example consists of two components:

- Raspberry Pi Pico 2 firmware
- Python host script (Reader)

Raspberry Pi SBCs or x86_64 lack built-in ADCs. The Pi Pico 2 acts as an ADC reader, converting the voltage from the SWC into a USB stream.

This example is based on universal wireless steering wheel controls and Key1/Key2 readings from the transmitter.

## Raspberry Pi Pico 2

A resistive ladder network where each button press alters the resistance, resulting in a specific voltage drop on the ADC line. Pi Pico2 continuously reads the analog voltage from the SWC, packs the raw data into binary frames and transmits them over USB CDC to the host machine.

The firmware is written in C/C++. It utilizes a timer to poll the ADC pins every 10ms and then stream read values over USB CDC to the host machine.

The firmware enables pull-up resistors on the ADC pins to allow readings. Resistive ladder-based buttons typically have two wires, **Key1** and **Key2**, which should be connected to the Raspberry Pi Pico's ADC pins (the firmware uses GPIO26 and GPIO27). The circuit must also share a common ground for the resistance reading to work properly (the Raspberry Pi Pico's GND must be connected to the transmitter's GND).

## Reader

A Python script running on the host machine. It reads data from the USB stream from Pico2 with ADC read values, then translates them to the Hudiy API.

### Calibration mode

The Reader features a special calibration mode where, instead of connecting to the Hudiy API, it prints the raw ADC values read by the Pi Pico 2 directly to the console. These values can then be used to create your own custom button configuration within the script.

The Reader can be launched in calibration mode by passing the `--calibrate` command-line argument:

```bash
python3 resistive_swc.py --calibrate
```

## How to use

You can find pre-compiled firmware binary under the Releases section of the repository. The flashing procedure is described in Chapter 5.1 in the [Official Raspberry Pi Pico 2 datasheet](https://pip-assets.raspberrypi.com/categories/1005-raspberry-pi-pico-2/documents/RP-008299-DS-2-pico-2-datasheet.pdf).

To use the Reader script on host machine, the following dependencies must be installed:

```bash
sudo apt install -y python3-serial python3-protobuf python3-websocket
```

By default, the Reader reads from `/dev/ttyACM0` - it can be changed in the source code.

### Autostart

The scripts can be configured to run automatically at system startup, for example, by adding it to **$HOME/.config/labwc/autostart**

```bash
python3 /home/pi/hudiy/examples/resistive_swc/ResistiveSwc.py &
```

*Note: Update the path to ResistiveSwc.py to match your local file location.*
