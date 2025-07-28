#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self.coverart_index = 0
        self.coverart = None
        self.coverart2 = None

        with open("assets/coverart.png", "rb") as f:
            self.coverart = f.read()

        with open("assets/coverart2.png", "rb") as f:
            self.coverart2 = f.read()

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        set_status_subscriptions = hudiy_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.COVERARTS)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

    def on_coverart_request(self, client, message):
        print(
            "coverart request: request code: {}, artist: {}, album: {}, title: {}, source: {}"
            .format(message.request_code, message.artist, message.album,
                    message.title, message.source))

        coverart_response = hudiy_api.CoverartResponse()
        coverart_response.request_code = message.request_code

        if self.coverart_index == 0:
            self.coverart_index = 1
            coverart_response.coverart = self.coverart
        else:
            self.coverart_index = 0
            coverart_response.coverart = self.coverart2

        client.send(hudiy_api.MESSAGE_COVERART_RESPONSE, 0,
                    coverart_response.SerializeToString())


def main():
    client = Client("coverarts example")
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
