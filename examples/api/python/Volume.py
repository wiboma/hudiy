#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._volume_up = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.control_volume(client)

    def control_volume(self, client):
        self._volume_up = not self._volume_up

        dispatch_action = hudiy_api.DispatchAction()
        dispatch_action.action = "output_volume_up" if self._volume_up else "output_volume_down"
        client.send(hudiy_api.MESSAGE_DISPATCH_ACTION, 0,
                    dispatch_action.SerializeToString())

        self._timer = threading.Timer(5, self.control_volume, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("Volume")
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
