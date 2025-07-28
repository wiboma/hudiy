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

        set_equalizer_preset = hudiy_api.SetEqualizerPreset()
        set_equalizer_preset.name = "Flat"
        client.send(hudiy_api.MESSAGE_SET_EQUALIZER_PRESET, 0,
                    set_equalizer_preset.SerializeToString())


def main():
    client = Client("equalizer preset example")
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
