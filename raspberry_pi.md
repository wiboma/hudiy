# Raspberry Pi

## Table of Contents

- [Introduction](#introduction)
- [Supported Raspberry Pi variants](#supported-raspberry-pi-variants)
- [Requirements](#requirements)
- [Desktop vs Console](#desktop-vs-console)
- [Hands-free Bluetooth profile](#hands-free-bluetooth-profile)

## Introduction

Early versions of Hudiy were designed for the Raspberry Pi 4 and Raspberry Pi 5. Thanks to optimizations introduced in version 2.8, Hudiy now also runs on older variants, such as the Pi 3B+, Pi 3B, and Pi Zero 2.

Across all Raspberry Pi models, Hudiy utilizes hardware acceleration for rendering, ensuring a smooth user experience.

The maximum supported resolution per screen is 1920x1080. However, with DRM video rendering enabled (Pi 4 and Pi 5 only), Hudiy offers **experimental** 2K and 4K support for Android Auto projection (see [Main Configuration](main_configuration.md#androidauto) for more details).

## Supported Raspberry Pi variants

### Raspberry Pi 5

Hudiy supports all Raspberry Pi 5 variants (1GB, 2GB, 4GB, 8GB, and 16GB).

Related variants, such as the Compute Module 5, are based on the same SoC (BCM2712). From Hudiy's perspective, there is no functional difference between running on a Raspberry Pi 5 or on a CM5.

The supported operating systems for the Raspberry Pi 5 are Raspberry Pi OS Trixie 64-bit Desktop and Raspberry Pi OS Bookworm 64-bit Desktop.

### Raspberry Pi 4

Hudiy supports all Raspberry Pi 4B variants (1GB, 2GB, 4GB and 8GB).

Related variants, such as the Compute Module 4, are based on the same SoC (BCM2711). From Hudiy's perspective, there is no functional difference between running on a Raspberry Pi 4B or on a CM4.

The supported operating systems for the Raspberry Pi 4 are Raspberry Pi OS Trixie 64-bit Desktop and Raspberry Pi OS Bookworm 64-bit Desktop.

### Raspberry Pi 3B+

Starting with version 2.8, Hudiy also supports the Raspberry Pi 3B+ variant. The supported operating system for the Raspberry Pi 3B+ is Raspberry Pi OS Trixie 64-bit Desktop.

Due to the less powerful CPU (in comparison to Pi 4B and Pi 5), the equalizer module is disabled by default.

Due to limited GPU hardware (in comparison to Pi 4B and Pi 5), Hudiy launches in EGL mode after installation. This means the desktop environment is disabled to save GPU resources. Since EGL mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled. You can still enable the desktop using the raspi-config tool but running Hudiy in a desktop environment is not recommended. We also recommend using lower screen resolutions (e.g., 800x480 or 1024x600).

Hudiy utilizes hardware acceleration, but due to I/O limitations, we recommend using projection (Android Auto and CarPlay) at 30FPS and lower resolutions.

### Raspberry Pi 3B

Starting with version 2.8, Hudiy also supports the Raspberry Pi 3B variant. The supported operating system for the Raspberry Pi 3B is Raspberry Pi OS Trixie 64-bit Desktop.

Due to the less powerful CPU (in comparison to Pi 4B and Pi 5), the equalizer module is disabled by default.

Due to limited GPU hardware (in comparison to Pi 4B and Pi 5), Hudiy launches in EGL mode after installation. This means the desktop environment is disabled to save GPU resources. Since EGL mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled. You can still enable the desktop using the raspi-config tool but running Hudiy in a desktop environment is not recommended. We also recommend using lower screen resolutions (e.g., 800x480).

The Raspberry Pi 3B is limited to 2.4GHz Wi-Fi (hardware limitation), which significantly restricts bandwidth (theoretically maxing out at 54Mbps). The combination of these Wi-Fi speeds and the Pi's I/O limitations means it is recommended to run projection (both Android Auto and CarPlay) at 30FPS and use lower screen resolutions. For better performance of Android Auto, you can use an external USB Wi-Fi module with 5GHz support or stick to a wired connection. Also you can consider configuring 40MHz channel width in [Main Configuration](main_configuration.md#hotspot). It will increase throughput but may also increase sensitivity to interference.

```json
{
    "channelConfigurationType" : "MANUAL",
    "channelBandwidth" : "40MHz",
    "channel" : 1
}
```

### Raspberry Pi Zero 2

Starting with version 2.8, Hudiy also supports the Raspberry Pi Zero 2 variant. The supported operating system for the Raspberry Pi Zero 2 is Raspberry Pi OS Trixie 64-bit Desktop.

Due to the less powerful CPU (in comparison to Pi 4B and Pi 5), the equalizer module is disabled by default.

Due to limited GPU hardware (in comparison to Pi 4B and Pi 5), Hudiy launches in EGL mode after installation. This means the desktop environment is disabled to save GPU resources. Since EGL mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled. You can still enable the desktop using the raspi-config tool but running Hudiy in a desktop environment is not recommended. We also recommend using lower screen resolutions (e.g., 800x480).

The Raspberry Pi Zero 2 is limited to 2.4GHz Wi-Fi (hardware limitation), which significantly restricts bandwidth (theoretically maxing out at 54Mbps). The combination of these Wi-Fi speeds and the Pi's I/O limitations means it is recommended to run projection (both Android Auto and CarPlay) at 30FPS and use lower screen resolutions. For better performance of Android Auto, you can use an external USB Wi-Fi module with 5GHz support or stick to a wired connection. Also you can consider configuring 40MHz channel width in [Main Configuration](main_configuration.md#hotspot). It will increase throughput but may also increase sensitivity to interference.

```json
{
    "channelConfigurationType" : "MANUAL",
    "channelBandwidth" : "40MHz",
    "channel" : 1
}
```

The Pi Zero 2 SiP (RP3A0) uses the BCM2710A1 (from the Raspberry Pi 3B), but it is downclocked by default. To improve performance on the Pi Zero 2, you can consider [overclocking](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking) it to match Pi 3B clock speeds.

Due to the limited amount of RAM (512MB), we recommend exercising caution when adding custom extensions (Overlays, Widgets, Applications) to avoid exhausting available system memory.

## Requirements

**Mandatory:**

- Supported Raspberry Pi variant
- Clean, unmodified installation of the official Raspberry Pi OS Trixie Desktop 64 bit (for Pi 5, Pi 4, Pi 3B+, Pi 3B, Pi Zero 2) or Raspberry Pi OS Bookworm Desktop 64 bit (for Pi 5, Pi 4)
- 8GB of free storage space
- Display with resolution up to 1920x1080

**Optional:**

- RTL-SDR dongle for FM Radio
- CarlinKit CPC-200 CCPA or Autokit dongle for CarPlay
- Microphone for Hands-Free calling and voice assistants
- USB or Bluetooth ELM327 adapter for OBD-II communication

## Desktop vs Console

To save GPU resources on Pi Zero 2, Pi 3B and Pi 3B+, Hudiy launches in console (EGL) mode. This means the desktop environment is disabled for these variants after installation. You can still enable the desktop using the raspi-config tool, but running Hudiy in a desktop environment on the Pi Zero 2, Pi 3B, and Pi 3B+ is not recommended.

Since console mode supports a maximum of one application window and one screen, the splash application (used for displaying a custom logo before Hudiy starts) is disabled in this mode.

In console mode, screen configuration (such as resolution and refresh rate) must be performed directly in the [/boot/firmware/cmdline.txt](https://www.raspberrypi.com/documentation/computers/configuration.html#set-the-kms-display-mode) file.

In console mode, Hudiy is launched via the `hudiy.service` systemd unit. In desktop mode, startup is handled by the labwc autostart file ($HOME/.config/labwc/autostart).

### Raspberry Pi 4 and Raspberry Pi 5

Raspberry Pi 4 and Raspberry Pi 5 have more powerful GPUs and can easily handle Hudiy in desktop mode. This is the recommended configuration for these models.

Based on our observations, there is no noticeable difference in boot times between desktop and console modes. Furthermore, using and configuring the system in desktop mode is significantly more user-friendly. Desktop mode can also handle multiple windows simultaneously and supports multiple screens.

## Hands-free Bluetooth

It appears that some Raspberry Pi models struggle with handling SCO traffic on the built-in Bluetooth chip. This is likely caused by a firmware issue or the PL011 controller (the UART interface used to communicate with the Bluetooth chip).

If you experience random disconnections during phone calls or see `hci0: hardware error 0x00` messages in `dmesg` ouput, consider adding [`dtoverlay=miniuart-bt`](https://www.raspberrypi.com/documentation/computers/configuration.html#uarts-and-device-tree) to /boot/firmware/config.txt.

The Raspberry Pi 3B and Pi Zero 2 route SCO audio traffic via PCM. Hudiy provides a `hcisco.service` systemd unit to reconfigure the Bluetooth controller (via hcitool) to use SCO over HCI instead. The service runs automatically for these Raspberry Pi variants.

SCO over HCI seems to be default mode for Raspberry Pi 3B+, Raspberry Pi 4 and Raspberry Pi 5.
