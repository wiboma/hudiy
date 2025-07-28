#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._enabled = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.toggle_dark_mode(client)

    def toggle_dark_mode(self, client):
        self._enabled = not self._enabled

        set_dark_mode = hudiy_api.SetDarkMode()
        set_dark_mode.enabled = self._enabled
        client.send(hudiy_api.MESSAGE_SET_DARK_MODE, 0,
                    set_dark_mode.SerializeToString())

        self._timer = threading.Timer(10, self.toggle_dark_mode, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("dark mode example")
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
