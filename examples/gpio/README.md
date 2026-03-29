# Description

This directory contains examples of using the Hudiy API with GPIO.

## Dependecies

To use the scripts, the following dependencies must be installed:

```bash
sudo apt install -y python3-gpiozero python3-protobuf python3-websocket
```

## How to run

After installing dependencies, simply run one of the examples, e. g.:

```bash
python3 ReverseCamera.py
```

### Autostart

The scripts can be configured to run automatically at system startup, for example, by adding it to **$HOME/.config/labwc/autostart** (before Hudiy startup)

```bash
python3 /home/pi/hudiy/examples/gpio/ReverseCamera.py &
```

*Note: Update the path to ReverseCamera.py to match your local file location.*
