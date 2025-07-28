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
            hudiy_api.SetStatusSubscriptions.Subscription.MEDIA)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

    def on_media_status(self, client, message):
        print("media status, is playing: {}, position label: {}, source: {}".
              format(message.is_playing, message.position_label,
                     message.source))

    def on_media_metadata(self, client, message):
        print(
            "media metadata, artist: {}, title: {}, album: {}, duration label: {}, coverart: {}"
            .format(message.artist, message.title, message.album,
                    message.duration_label, len(message.coverart)))


def main():
    client = Client("media data example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44406, use_websocket=True)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    main()
