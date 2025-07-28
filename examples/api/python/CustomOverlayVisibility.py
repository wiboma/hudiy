#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._visible = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.toggle_overlay_visibility(client)

    def toggle_overlay_visibility(self, client):
        self._visible = not self._visible

        set_custom_overlay_visibility = hudiy_api.SetCustomOverlayVisibility()
        # Overlay with this name must be available in overlays.json
        set_custom_overlay_visibility.identifier = "overlay2"
        set_custom_overlay_visibility.visibility = hudiy_api.OVERLAY_VISIBILITY_ALWAYS if self._visible else hudiy_api.OVERLAY_VISIBILITY_NONE
        client.send(hudiy_api.MESSAGE_SET_CUSTOM_OVERLAY_VISIBILITY, 0,
                    set_custom_overlay_visibility.SerializeToString())

        self._timer = threading.Timer(10, self.toggle_overlay_visibility,
                                      [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("custom overlay visibility example")
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
