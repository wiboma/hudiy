# Hudiy Configuration

## Table of Contents

- [Introduction](#introduction)
- [application](#application)
- [appearance](#appearance)
- [theme](#theme)
- [sound](#sound)
- [androidAuto](#androidauto)
- [hotspot](#hotspot)
- [equalizer](#equalizer)
- [notifications](#notifications)
- [fmRadio](#fmradio)
- [autobox](#autobox)
- [obd](#obd)
- [api](#api)
- [reverseCamera](#reversecamera)

## Introduction

This document describes the configuration of the Hudiy application.

The main configuration file is stored at `$HOME/.hudiy/share/config/main_configuration.json`.

The configuration is stored in JSON format.

## application

- `handednessOfTraffic`:  
    The side of the road on which the vehicle drives. This setting determines the default layout of the native UI, Android Auto, and CarPlay.

    Possible values:
    - "LEFT"
    - "RIGHT"

- `defaultAction`:  
    The default action for the initial screen dispatched when dashboards icon on bottom bar or home `h` key was pressed. If empty, the action of the default dashboard will be used.

- `showDashboardsIcon`:  
    Show/hide dashboards icon on bottom bar.

    Possible values:
    - true – the icon is visible
    - false – the icon is invisible

- `showMenuIcon`:  
    Show/hide main menu icon on bottom bar.

    Possible values:
    - true – the icon is visible
    - false – the icon is invisible

- `touchscreen`:  
    Indicates whether the system is equipped with a touchscreen.

    Possible values:
    - true – the system is equipped with a touchscreen  
    - false – the system is not equipped with a touchscreen

- `showCursor`:  
    Enables or disables rendering of the mouse cursor in the Hudiy application.

    Possible values:
    - true – enables cursor rendering  
    - false – disables cursor rendering

- `width`:  
    The width of the surface inside the application window that will be used to render the native UI.  
    This parameter is useful for split-screen configurations.

- `height`:  
    The height of the surface inside the application window that will be used to render the native UI.  
    This parameter is useful for split-screen configurations.

- `x`:  
    The x-coordinate (top-left corner, in pixels) of the UI inside the application window.

- `y`:  
    The y-coordinate (top-left corner, in pixels) of the UI inside the application window.

- `splitWithProjections`:  
    Determines the behavior of `KEY_TYPE_TOGGLE_INPUT_FOCUS`.

    Possible values:
    - true – Android Auto/CarPlay projection is configured to display next to the native UI  
    - false – Android Auto/CarPlay projection is configured to display on top of the native UI

- `windowWidth`:  
    The width of the application window. If set to 0, the maximum screen width will be used.

- `windowHeight`:  
    The height of the application window. If set to 0, the maximum screen height will be used.

- `handleKeyboardEvents`:  
    Enable or disable keyboard event handling. Key events injected via the API are not affected by this setting.

    Possible values:
    - true – Listen to keyboard events
    - false – Do not listen to keyboard events (it is still possible to inject key events via the API)

- `translationFile`:  
    Absolute path to the *.qm translation file generated from hudiy.ts.

## appearance

- `timeFormat`:  
    The format of the time displayed on the native UI.

    Possible values:
    - "12h"
    - "24h"

- `showClock`:  
    Shows or hides the clock on the bottom bar.

    Possible values:
    - true – show the clock on the bottom bar  
    - false – hide the clock on the bottom bar

- `fonts`:  
    A list of absolute paths to font files that will be loaded by the Hudiy application.  
    The loaded fonts can later be used for rendering custom icons defined for menus, shortcuts, and other elements.

## theme

- `darkThemeEnabled`:  
    Enables or disables the dark theme.

    Possible values:
    - true – the dark theme is enabled  
    - false – the dark theme is disabled and the light theme is used

- `darkContrastLevel`:  
    Color contrast level for the dark theme.

    Possible values:
    - A range between -1.0 and 1.0

- `darkSourceColor`:  
    The source color for the dark theme.

    Possible values:
    - Hex color code (RGB)

- `lightContrastLevel`:  
    Color contrast level for the light theme.

    Possible values:
    - A range between -1.0 and 1.0

- `lightSourceColor`:  
    The source color for the light theme.

    Possible values:
    - Hex color code (RGB)

- `availableColors`:  
    A list of predefined source colors that can later be selected in the settings.

    Possible values:
    - Array of hex color codes (RGB)

- `lightBackgroundsMap`:  
    An object (key-value pairs) that defines background images for each menu action in the light theme.

    Example values:
    ```json
    {
        "storage_music_player": "/home/hudiy/Pictures/backgrounds/light/background_for_storage_music_player.jpg",
        "fm_radio_player": "/home/hudiy/Pictures/backgrounds/light/fm_radio_player_background.jpg"
    }
    ```

- `darkBackgroundsMap`:  
    An object (key-value pairs) that defines background images for each menu action in the dark theme.  
    The key (property name) is the name of an action.  
    The value is the absolute path to the image file.

    Example values:
    ```json
    {
        "storage_music_player": "/home/hudiy/Pictures/backgrounds/dark/background_for_storage_music_player.jpg",
        "fm_radio_player": "/home/hudiy/Pictures/backgrounds/dark/fm_radio_player_background.jpg"
    }
    ```

- `defaultDarkBackground`:  
    The absolute path to the default background image file for the dark theme.  
    Backgrounds defined in `darkBackgroundsMap` take precedence.

- `defaultLightBackground`:  
    The absolute path to the default background image file for the light theme.  
    Backgrounds defined in `lightBackgroundsMap` take precedence.

- `darkBackgroundOpacity`:  
    The opacity level of background images in the dark theme. Applies to both `darkBackgroundsMap` and `defaultDarkBackground`.

- `lightBackgroundOpacity`:  
    The opacity level of background images in the light theme. Applies to both `lightBackgroundsMap` and `defaultLightBackground`.

## sound

- `startupSoundFile`:  
    The absolute path to the **.wav** file that will be played immediately after the application starts.

- `notificationSoundFile`:  
    The absolute path to the **.wav** file that will be played for notifications with sound enabled (e.g., Bluetooth connection).

- `volumeSinkName`:  
    The name of the sink from `pactl list sinks` that the Hudiy app will use to control volume.  
    If any virtual sinks are defined in the system (e.g., for applying equalization), it is recommended to specify the sink associated with the actual audio device here. Use system-default audio sink if not provided.

- `playbackSinkName`:  
    The name of the sink from `pactl list sinks` where all audio from the Hudiy app will be routed. Use system-default audio sink if not provided.

    *Note: A2DP playback is handled directly by PipeWire and will be routed to the default sink.*

- `sourceName`:  
    The name of the source from `pactl list sources` that the Hudiy app will use to capture audio and control input volume. Use system-default audio source if not provided.

    *Note: HFP is handled directly by PipeWire and will use the default source.*

- `sourceMaxVolume`:  
    The maximum percentage value of the volume that can be set for the source.

- `sinkMaxVolume`:  
    The maximum percentage value of the volume that can be set for the sink.

- `outputVolumeStep`:  
    The value that will be added to or subtracted from the current output volume level when output volume actions are triggered.

- `inputVolumeStep`:  
    The value that will be added to or subtracted from the current input volume level when input volume actions are triggered.

- `subwooferBalanceStep`:  
    The value that will be added to or subtracted from the current subwoofer (LFE) balance level.

    *Note: Subwoofer balance can be controlled in the Hudiy app only if PipeWire reports the availability of LFE.*

- `balanceStep`:  
    The value that will be added to or subtracted from the current balance level.

    *Note: Balance can be controlled in the Hudiy app only if PipeWire reports the availability of stereo (FRONT LEFT, FRONT RIGHT), 4.0 (FRONT LEFT, FRONT RIGHT, REAR LEFT, REAR RIGHT), or 4.1 (FRONT LEFT, FRONT RIGHT, REAR LEFT, REAR RIGHT, LFE) speaker setups.*

- `fadeStep`:  
    The value that will be added to or subtracted from the current fader level.

    *Note: Fade can be controlled in the Hudiy app only when PipeWire reports the availability of a 4.0 (FRONT LEFT, FRONT RIGHT, REAR LEFT, REAR RIGHT) or 4.1 (FRONT LEFT, FRONT RIGHT, REAR LEFT, REAR RIGHT, LFE) speaker setup.*

- `subwooferBalance`:  
    The last stored value of subwoofer (LFE) balance. It will be restored during Hudiy startup.

- `fade`:  
    The last stored value of fade. It will be restored during Hudiy startup.

- `balance`:  
    The last stored value of balance. It will be restored during Hudiy startup.

- `storageMusicAutoplay`:  
    Enables or disables automatic playback of the storage music player after Hudiy startup  
    (only if the last audio source was the storage music player and the last played media file is still available).

    Possible values:
    - true – start playback of the storage music player after Hudiy startup (only if the last audio source was the storage music player and the last played media file is available)  
    - false – do not start playback of the storage music player after Hudiy startup

- `fmRadioAutoplay`:  
    Enables or disables automatic playback of FM radio after Hudiy startup  
    (only if the last audio source was FM radio).

    Possible values:
    - true – start playback of FM radio after Hudiy startup (only if the last audio source was FM radio)  
    - false – do not start playback of FM radio after Hudiy startup

- `ringtoneFile`:  
    The absolute path to the **.wav** file that will be played during an incoming call.

## androidAuto

- `speechAudio`:  
    Plays audio received from the speech (navigation, assistant) endpoint.

    Possible values:
    - true – play audio received from the speech endpoint  
    - false – let the phone decide how to route audio from the speech endpoint (e.g., via A2DP, Jack)

- `mediaAudio`:  
    Plays audio received from the media endpoint.

    Possible values:
    - true – play audio received from the media endpoint  
    - false – let the phone decide how to route audio from the media endpoint (e.g., via A2DP, Jack)

- `resolution`:  
    Resolution of the video stream used for projection.

    Possible values:
    - "480p"
    - "720p"
    - "1080p"

- `bluetoothAddress`:  
    The address of the Bluetooth adapter that will be sent to the Bluetooth endpoint as the head unit's address.  
    If empty, the address of the primary local Bluetooth adapter will be used.

    Example value:
    - 00:01:02:03:04:05

- `autostart`:  
    Automatically triggers a USB or wireless connection to Android Auto.

- `dpi`:  
    Scale of the Android Auto interface. A higher value increases the size of the Android Auto interface.

- `widthMargin`:  
    Horizontal margins of the video stream used for projection that will be subtracted from the total resolution.  
    Left margin = `widthMargin / 2`, right margin = `widthMargin / 2`.

    Useful for setting a custom projection resolution, e.g., 1024×600, 1280×480, or 1920×720.

- `heightMargin`:  
    Vertical margins of the video stream used for projection that will be subtracted from the total resolution.  
    Top margin = `heightMargin / 2`, bottom margin = `heightMargin / 2`.

    Useful for setting a custom projection resolution or the size of the rendering surface, e.g., 1024×600, 1280×480, or 1920×720.

- `width`:  
    Width of the rendering surface for the projection.

- `height`:  
    Height of the rendering surface for the projection.

- `x`:  
    The x-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

- `y`:  
    The y-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

## hotspot

- `enabled`:  
    Enables or disables the hotspot.  
    The hotspot will be automatically disabled when the Hudiy application exits.

    Possible values:
    - true – the hotspot is enabled  
    - false – the hotspot is disabled

- `hardwareAddress`:  
    The hardware address of the wireless adapter that will be used to serve the hotspot.

    If the hotspot is disabled, this address will be forwarded to Android Auto as the BSSID of the external wireless network.

    Example value:
    - 00:01:02:03:04:05

- `ipAddress`:  
    The gateway IP address.

    Example value:
    - 192.168.12.1

- `passphrase`:  
    The passphrase for the hotspot if enabled, or the passphrase of the external wireless network if the hotspot is disabled.

- `ssid`:  
    The SSID of the hotspot if enabled, or the SSID of the external wireless network used for wireless Android Auto if the hotspot is disabled.

- `bandwidth`:  
    The bandwidth of the hotspot if enabled, or the bandwidth of the external wireless network if the hotspot is disabled.

    Possible values:
    - "A" – 5GHz network  
    - "BG" – 2.4GHz network

## equalizer

- `enabled`:  
    Enables or disables the equalizer.

    Possible values:
    - true – the equalizer is enabled  
    - false – the equalizer is disabled

- `step`:  
    The value that will be added to or subtracted from the current level of a particular band.

- `minValue`:  
    The minimum value allowed for the bands.

- `maxValue`:  
    The maximum value allowed for the bands.

- `band25`:  
    Current value for the 25 Hz band.

- `band40`:  
    Current value for the 40 Hz band.

- `band63`:  
    Current value for the 63 Hz band.

- `band100`:  
    Current value for the 100 Hz band.

- `band160`:  
    Current value for the 160 Hz band.

- `band250`:  
    Current value for the 250 Hz band.

- `band400`:  
    Current value for the 400 Hz band.

- `band630`:  
    Current value for the 630 Hz band.

- `band1000`:  
    Current value for the 1000 Hz band.

- `band1600`:  
    Current value for the 1600 Hz band.

- `band2500`:  
    Current value for the 2500 Hz band.

- `band4000`:  
    Current value for the 4000 Hz band.

- `band6300`:  
    Current value for the 6300 Hz band.

- `band10000`:  
    Current value for the 10000 Hz band.

- `band16000`:  
    Current value for the 16000 Hz band.

### Presets

Each preset includes a name and values for each frequency band:

- `name`:  
- `band25`:  
- `band40`:  
- ...  
- `band16000`:  

## notifications

- `outputVolumeToast`:  
    Enables or disables the display of output volume toast notifications.

    Possible values:
    - true – output volume toasts will be displayed  
    - false – output volume toasts will not be displayed

- `inputVolumeToast`:  
    Enables or disables the display of input volume toast notifications.

    Possible values:
    - true – input volume toasts will be displayed  
    - false – input volume toasts will not be displayed

- `nowPlaying`:  
    Enables or disables the display of "now playing" notifications.

    Possible values:
    - true – "now playing" notifications will be displayed  
    - false – "now playing" notifications will not be displayed

- `notificationDuration`:  
    Duration (in seconds) for which notifications are displayed.

- `toastDuration`:  
    Duration (in seconds) for which toasts are displayed.

## fmRadio

- `bandwidth`:  
    FM broadcast band.

    Possible values:
    - "EU"  
        - Start: 87.5 MHz  
        - End: 108.0 MHz  
        - Step: 50 kHz

    - "JP"  
        - Start: 76.0 MHz  
        - End: 95.0 MHz  
        - Step: 100 kHz

    - "US"  
        - Start: 87.9 MHz  
        - End: 107.9 MHz  
        - Step: 200 kHz

    - "ITU1"  
        - Start: 87.5 MHz  
        - End: 108.0 MHz  
        - Step: 50 kHz

    - "ITU2"  
        - Start: 87.5 MHz  
        - End: 107.9 MHz  
        - Step: 50 kHz

- `squelchLevel`:  
    The threshold that determines when the receiver outputs audio.

- `squelchLimit`:  
    The sensitivity of frequency scanning.

- `rdsEnabled`:  
    Enables or disables receiving and decoding of the RDS signal.

    Possible values:
    - true – RDS reception and decoding is enabled  
    - false – RDS reception and decoding is disabled

- `autoGain`:  
    Allows the device to automatically select the gain level.

    Possible values:
    - true – the device will automatically select the gain level; the `gain` value is ignored  
    - false – the device will use the gain value specified by the `gain` parameter

- `gain`:  
    The gain level of the device.

- `presets`:  
    An array of objects with favorite radio stations.
    - `name`:  
        Name of the preset visible in favorites menu.

    - `frequency`:  
        Frequency of the radio station.

## autobox

- `dpi`:  
    Specifies the DPI of the screen on which the projection will be displayed.

- `width`:  
    Width of the rendering surface for the projection.

- `height`:  
    Height of the rendering surface for the projection.

- `x`:  
    The x-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

- `y`:  
    The y-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

- `oemName`:  
    Label of the back button in the CarPlay menu.  
    The icon of the button can be changed by replacing the file at `$HOME/.hudiy/share/autobox/logo.png`.

- `autoWirelessConnection`:  
    Automatically triggers a wireless connection to CarPlay.

- `vendorId`:  
    USB Vendor ID (VID) of the autobox device.

- `productId`:  
    USB Product ID (PID) of the autobox device.

- `bandwidth`:  
    Bandwidth of the wireless hotspot on the autobox device.

    Possible values:
    - "AUTO"  
    - "2.4GHz"  
    - "5GHz"

## obd

- `deviceType`:  
    Type of the ELM327 device.

    Possible values:
    - "SERIAL"  
    - "RFCOMM"

- `serialDescriptor`:  
    Descriptor of the ELM327 device when using the SERIAL type.

    Example value:  
    `/dev/ttyUSB0`

- `baudrate`:  
    Baud rate of the ELM327 serial device.

- `rfcommAddress`:  
    MAC address of the ELM327 device when using the RFCOMM type.

    *Note: Most Bluetooth ELM327 devices must be paired first.*

- `rfcommChannel`:  
    RFCOMM channel of the ELM327 device.

- `maxInvalidResponseCount`:  
    Number of invalid responses from the ELM327 device after which the connection will be reset.

- `startupSequence`:  
    Commands that will be sent to the ELM327 device after the connection is established.

## api

- `tcpEndpointPort`:  
    The listening port of the TCP server for the API endpoint.

- `webSocketEndpointPort`:  
    The listening port of the WebSocket server for the API endpoint.

## reverseCamera

- `width`:  
    Width of the rendering surface for the projection.

- `height`:  
    Height of the rendering surface for the projection.

- `x`:  
    The x-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

- `y`:  
    The y-coordinate (top-left corner, in pixels) of the rendering surface inside the application window.

- `pipeline`:  
    GStreamer pipeline that will be used to obtain the reverse camera stream.

    *Note: The pipeline must always output to a `qml6glsink` named `video-sink`:*  
    `qml6glsink name=video-sink`
