#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._action = "example_api_action"
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_action_request = hudiy_api.RegisterActionRequest()
        register_action_request.action = self._action

        client.send(hudiy_api.MESSAGE_REGISTER_ACTION_REQUEST, 0,
                    register_action_request.SerializeToString())

    def on_register_action_response(self, client, message):
        print("register action response, result: {}, action: {}".format(
            message.result, message.action))

        if message.result:
            print("action successfully registered")
            self.trigger_action(client)

    def on_dispatch_action(self, client, message):
        print("dispatch action received, action: {}".format(message.action))

    def trigger_action(self, client):
        dispatch_action = hudiy_api.DispatchAction()
        dispatch_action.action = self._action
        client.send(hudiy_api.MESSAGE_DISPATCH_ACTION, 0,
                    dispatch_action.SerializeToString())

        self._timer = threading.Timer(5, self.trigger_action, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("dispatch action example")
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
