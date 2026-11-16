# Radxa

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)

## Introduction

Hudiy has been fully tested on the Radxa Rock 4B and the official Debian Bookworm vendor image.

After installation, Hudiy launches in EGL mode. This means the desktop environment is disabled to save GPU resources and provide full performance of hardware acceleration and zero-copy. Since EGL mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled.

## Requirements

**Mandatory:**

- Radxa Rock 4B
- Clean, unmodified installation of the official Radxa **Debian Bookworm** OS 64 bit
- 8GB of free storage space
- Display with resolution up to 1920x1080

**Optional:**

- RTL-SDR dongle for FM Radio and DAB Radio
- CarlinKit CPC-200 CCPA or Autokit dongle for CarPlay
- Microphone for Hands-Free calling and voice assistants
- USB or Bluetooth ELM327 adapter for OBD-II communication
