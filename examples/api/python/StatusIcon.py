#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._icon_id = None
        self._icon_visible = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_status_icon_request = hudiy_api.RegisterStatusIconRequest()
        register_status_icon_request.description = "Status icon from API example"
        register_status_icon_request.icon_name = "info"
        register_status_icon_request.icon_font_family = "Material Symbols Rounded"

        client.send(hudiy_api.MESSAGE_REGISTER_STATUS_ICON_REQUEST, 0,
                    register_status_icon_request.SerializeToString())

    def on_register_status_icon_response(self, client, message):
        print("register status icon response, result: {}, icon id: {}".format(
            message.result, message.id))
        self._icon_id = message.id

        if message.result == hudiy_api.RegisterStatusIconResponse.REGISTER_STATUS_ICON_RESULT_OK:
            print("icon successfully registered")
            self.toggle_icon_visibility(client)

    def toggle_icon_visibility(self, client):
        self._icon_visible = not self._icon_visible

        change_status_icon_state = hudiy_api.ChangeStatusIconState()
        change_status_icon_state.id = self._icon_id
        change_status_icon_state.visible = self._icon_visible
        client.send(hudiy_api.MESSAGE_CHANGE_STATUS_ICON_STATE, 0,
                    change_status_icon_state.SerializeToString())

        self._timer = threading.Timer(5, self.toggle_icon_visibility, [client])
        self._timer.start()

    def get_icon_id(self):
        return self._icon_id

    def get_timer(self):
        return self._timer


def main():
    client = Client("status icon example")
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

    if event_handler.get_icon_id() is not None:
        unregister_status_icon = hudiy_api.UnregisterStatusIcon()
        unregister_status_icon.id = event_handler.get_icon_id()
        client.send(hudiy_api.MESSAGE_UNREGISTER_STATUS_ICON, 0,
                    unregister_status_icon.SerializeToString())

    client.disconnect()


if __name__ == "__main__":
    main()
