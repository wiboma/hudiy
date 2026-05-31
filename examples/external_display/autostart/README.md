# Description

This directory contains examples for automatically launching the Web Viewer and HTTP server at system startup. Depending on how Hudiy is used (Console mode or Desktop mode), two variants have been prepared: a script and systemd user services.

See [x86_64](../../../x86_64.md), [Raspberry Pi](../../../raspberry_pi.md) and [Splash](../../../README.md#splash) docs for more details about Hudiy startup.

## Console mode

In console mode, Hudiy starts as a systemd user service (hudiy.service). Since EGLFS is used to display the Hudiy interface in Console mode, the Web Viewer should be configured to use EGLFS in headless mode to avoid blocking GPU resources. An example headless mode configuration can be found in the `eglfs_web_viewer_acm0_headless.json` file. Copy it to `$HOME/.hudiy/share` or adjust the path in `external-display-acm0.service`. Also, please double-check that the resolution in `eglfs_web_viewer_acm0_headless.json` matches the resolution of your display.

Autostart in Console mode is split into two services:

- A service for the HTTP server hosting the widgets - `widget-http.service`.

- A service for the Web Viewer communicating with the Raspberry Pi Pico 2 via `/dev/ttyACM0` - `external-display-acm0.service`.  

    The service will automatically restart the Web Viewer if it exits with a non-zero code (e.g., due to a communication error with the Raspberry Pi Pico 2 or if it gets disconnected).

    It also depends on `widget-http.service`, ensuring it will only start after http server is running.

Copy the *.service files to the `$HOME/.config/systemd/user/` directory:

```bash
mkdir -p $HOME/.config/systemd/user/
cp *.service $HOME/.config/systemd/user/
```

and then run the following commands:

```bash
systemctl --user daemon-reload
systemctl --user enable --now widget-http.service external-display-acm0.service
```

*Note: Please remember to adjust the paths accordingly.*

## Desktop mode

In Desktop mode, since Wayland handles GPU resource allocation, the Web Viewer and Hudiy can be started at any time without the risk of monopolizing graphics resources.

The `external-display-acm0.sh` script serves as an autostart example for Desktop mode. The script starts the HTTP server and then the Web Viewer, monitoring its operation and automatically restarting it if it exits with a non-zero code.

To run the script, you can either add it to $HOME/.config/labwc/autostart (*please note that the script must be run in the background by appending `&` so it doesn't block other autostart commands*) or copy the `external-display-acm0.desktop` file to `$HOME/.config/autostart`.

*Note: Please remember to adjust the paths accordingly.*
