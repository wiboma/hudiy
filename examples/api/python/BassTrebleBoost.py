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

        set_bass_treble_boost = hudiy_api.SetBassTrebleBoost()
        set_bass_treble_boost.bass_gain = 6
        set_bass_treble_boost.bass_frequency = 120

        set_bass_treble_boost.treble_gain = 3
        set_bass_treble_boost.treble_frequency = 10000
        client.send(hudiy_api.MESSAGE_SET_BASS_TREBLE_BOOST, 0,
                    set_bass_treble_boost.SerializeToString())


def main():
    client = Client("bass treble boost example")
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
