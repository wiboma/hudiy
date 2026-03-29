import common.Api_pb2 as hudiy_api
import time
from common.Client import Client, ClientEventHandler
from gpiozero import Button, RotaryEncoder


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._back_button = Button(26, bounce_time=0.05)
        self._left_button = Button(16, bounce_time=0.05)
        self._down_button = Button(25, bounce_time=0.05)
        self._right_button = Button(24, bounce_time=0.05)
        self._up_button = Button(23, bounce_time=0.05)
        self._encoder_button = Button(22, bounce_time=0.1)
        self._encoder = RotaryEncoder(a=17, b=27, max_steps=0)

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self._back_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_BACK, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._back_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_BACK, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._left_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_LEFT, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._left_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_LEFT, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._down_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_DOWN, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._down_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_DOWN, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._right_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_RIGHT, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._right_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_RIGHT, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._up_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_UP, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._up_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_UP, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._encoder_button.when_pressed = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_ENTER, hudiy_api.KeyEvent.
            EVENT_TYPE_PRESS)
        self._encoder_button.when_released = lambda: self.on_button_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_ENTER, hudiy_api.KeyEvent.
            EVENT_TYPE_RELEASE)

        self._encoder.when_rotated_clockwise = lambda: self.on_rotation_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_SCROLL_LEFT)
        self._encoder.when_rotated_counter_clockwise = lambda: self.on_rotation_event(
            client, hudiy_api.KeyEvent.KEY_TYPE_SCROLL_RIGHT)

    def on_button_event(self, client, key_type, event_type):
        key_event = hudiy_api.KeyEvent()
        key_event.key_type = key_type
        key_event.event_type = event_type
        client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                    key_event.SerializeToString())

    def on_rotation_event(self, client, key_type):
        key_event = hudiy_api.KeyEvent()
        key_event.key_type = key_type

        key_event.event_type = hudiy_api.KeyEvent.EVENT_TYPE_PRESS
        client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                    key_event.SerializeToString())

        key_event.event_type = hudiy_api.KeyEvent.EVENT_TYPE_RELEASE
        client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                    key_event.SerializeToString())


def main():
    client = Client("keys gpio example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)

    try:
        while True:
            try:
                client.connect('127.0.0.1', 44405)
                while True:
                    if not client.wait_for_message():
                        break
            except Exception:
                pass
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
