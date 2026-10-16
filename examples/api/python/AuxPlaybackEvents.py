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
            hudiy_api.SetStatusSubscriptions.Subscription.AUX)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

    def on_aux_playback_event(self, client, message):
        print("aux playback event: {}".format(message.event_type))


def main():
    client = Client("aux playback events example")
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
