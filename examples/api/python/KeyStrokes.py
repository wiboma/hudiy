#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


def listen_for_key_events(client):
    while True:
        key_type = None
        entered_key_type = input(
            "Enter key type (type break to exit): ").upper()

        if entered_key_type == "UP":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_UP
        elif entered_key_type == "DOWN":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_DOWN
        elif entered_key_type == "LEFT":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_LEFT
        elif entered_key_type == "RIGHT":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_RIGHT
        elif entered_key_type == "SCROLL_LEFT":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_SCROLL_LEFT
        elif entered_key_type == "SCROLL_RIGHT":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_SCROLL_RIGHT
        elif entered_key_type == "ENTER":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_ENTER
        elif entered_key_type == "BACK":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_BACK
        elif entered_key_type == "HOME":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_HOME
        elif entered_key_type == "ANSWER_CALL":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_ANSWER_CALL
        elif entered_key_type == "PHONE_MENU":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_PHONE_MENU
        elif entered_key_type == "HANGUP_CALL":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_HANGUP_CALL
        elif entered_key_type == "PLAY":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_PLAY
        elif entered_key_type == "TOGGLE_PLAY":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_TOGGLE_PLAY
        elif entered_key_type == "PAUSE":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_PAUSE
        elif entered_key_type == "STOP":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_STOP
        elif entered_key_type == "PREVIOUS_TRACK":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_PREVIOUS_TRACK
        elif entered_key_type == "NEXT_TRACK":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_NEXT_TRACK
        elif entered_key_type == "MEDIA_MENU":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_MEDIA_MENU
        elif entered_key_type == "NAVIGATION_MENU":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_NAVIGATION_MENU
        elif entered_key_type == "VOICE_COMMAND":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_VOICE_COMMAND
        elif entered_key_type == "TOGGLE_INPUT_FOCUS":
            key_type = hudiy_api.KeyEvent.KEY_TYPE_TOGGLE_INPUT_FOCUS
        elif entered_key_type == "BREAK":
            print("Press Ctrl+C to exit...")
            return
        else:
            print("Invalid key")

        if key_type is not None:
            key_event = hudiy_api.KeyEvent()
            key_event.key_type = key_type

            key_event.event_type = hudiy_api.KeyEvent.EVENT_TYPE_PRESS
            client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                        key_event.SerializeToString())

            key_event.event_type = hudiy_api.KeyEvent.EVENT_TYPE_RELEASE
            client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                        key_event.SerializeToString())


class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        threading.Thread(target=listen_for_key_events, args=(client, )).start()


def main():
    client = Client("media data example")
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
