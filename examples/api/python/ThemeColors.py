#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._dark_mode = False
        self._color_toggle = False
        self._tick_counter = 0
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.run_loop(client)

    def run_loop(self, client):
        self._color_toggle = not self._color_toggle

        set_theme_colors = hudiy_api.SetThemeColors()

        if self._color_toggle:
            set_theme_colors.dark_theme_color = "#000000"
            set_theme_colors.light_theme_color = "#ffffff"
        else:
            set_theme_colors.dark_theme_color = "#ffffff"
            set_theme_colors.light_theme_color = "#000000"

        client.send(hudiy_api.MESSAGE_SET_THEME_COLORS, 0,
                    set_theme_colors.SerializeToString())

        if self._tick_counter % 4 == 0:
            self._dark_mode = not self._dark_mode
            set_dark_mode = hudiy_api.SetDarkMode()
            set_dark_mode.enabled = self._dark_mode
            client.send(hudiy_api.MESSAGE_SET_DARK_MODE, 0,
                        set_dark_mode.SerializeToString())

        self._tick_counter += 1

        self._timer = threading.Timer(5.0, self.run_loop, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("theme colors example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    if event_handler.get_timer() is not None:
        event_handler.get_timer().cancel()

    client.disconnect()


if __name__ == "__main__":
    main()
