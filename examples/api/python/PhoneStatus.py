#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        set_status_subscriptions = hudiy_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.PHONE)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

    def on_phone_connection_status(self, client, message):
        print("phone connection status: {}, name: {}".format(
            message.state, message.name))

    def on_phone_levels_status(self, client, message):
        print("phone levels status, battery: {}, signal strength: {}%".format(
            message.bettery_level, message.signal_level))

    def on_phone_voice_call_status(self, client, message):
        print("voice call status, state: {}, caller name: {}, caller id: {}".
              format(message.state, message.caller_name, message.caller_id))


def main():
    client = Client("phone status example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    main()
