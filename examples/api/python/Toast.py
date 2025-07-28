#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._toast_channel_id = None
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_toast_channel_request = hudiy_api.RegisterToastChannelRequest(
        )
        register_toast_channel_request.name = "Example Toast Channel"
        register_toast_channel_request.description = "Toast channel from API example"

        client.send(hudiy_api.MESSAGE_REGISTER_TOAST_CHANNEL_REQUEST, 0,
                    register_toast_channel_request.SerializeToString())

    def on_register_toast_channel_response(self, client, message):
        print(
            "register toast channel response, result: {}, icon id: {}".format(
                message.result, message.id))
        self._toast_channel_id = message.id

        if message.result == hudiy_api.RegisterToastChannelResponse.REGISTER_TOAST_CHANNEL_RESULT_OK:
            print("toast channel successfully registered")
            self.show_toast(client)

    def show_toast(self, client):
        show_toast = hudiy_api.ShowToast()
        show_toast.channel_id = self._toast_channel_id
        show_toast.message = "Hello World"
        show_toast.icon_font_family = "Material Symbols Rounded"
        show_toast.icon_name = "info"

        client.send(hudiy_api.MESSAGE_SHOW_TOAST, 0,
                    show_toast.SerializeToString())

        self._timer = threading.Timer(30, self.show_toast, [client])
        self._timer.start()

    def get_toast_channel_id(self):
        return self._toast_channel_id

    def get_timer(self):
        return self._timer


def main():
    client = Client("toast example")
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

    if event_handler.get_toast_channel_id() is not None:
        unregister_toast_channel = hudiy_api.UnregisterToastChannel()
        unregister_toast_channel.id = event_handler.get_toast_channel_id()
        client.send(hudiy_api.MESSAGE_UNREGISTER_TOAST_CHANNEL, 0,
                    unregister_toast_channel.SerializeToString())

    client.disconnect()


if __name__ == "__main__":
    main()
