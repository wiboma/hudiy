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

        aux_metadata = hudiy_api.SetAuxMetadata()
        aux_metadata.title = "Title for AUX player"
        aux_metadata.album = "Album for AUX player"
        aux_metadata.artist = "Artist for AUX player"
        client.send(hudiy_api.MESSAGE_SET_AUX_METADATA, 0,
                    aux_metadata.SerializeToString())


def main():
    client = Client("aux metadata example")
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
