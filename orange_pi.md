# Orange Pi

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)

## Introduction

Hudiy has been fully tested on the Orange Pi 4 Pro and the official Debian Trixie vendor image.

After installation, Hudiy launches in EGL mode. This means the desktop environment is disabled to save GPU resources and provide full performance of hardware acceleration and zero-copy. Since EGL mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled.

By default, Orange Pi kernels do not include compiled kernel modules for **multi-touch** and **optical drives**. To use multi-touch functionality in Android Auto and the Audio CD player, you need to compile the missing modules (`hid-multitouch.ko`, `sr_mod.ko`) for the current Linux kernel version on the device.

## Requirements

**Mandatory:**

- Orange Pi 4 Pro
- Clean, unmodified installation of the official Orange Pi **Debian Trixie** OS 64 bit
- 8GB of free storage space
- Display with resolution up to 1920x1080

**Optional:**

- RTL-SDR dongle for FM Radio and DAB Radio
- CarlinKit CPC-200 CCPA or Autokit dongle for CarPlay
- Microphone for Hands-Free calling and voice assistants
- USB or Bluetooth ELM327 adapter for OBD-II communication
