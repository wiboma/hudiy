import common.Api_pb2 as hudiy_api
import time
from common.Client import Client, ClientEventHandler
from gpiozero import Button


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._gpio_button = Button(26, bounce_time=0.05)

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.send_dark_mode_status(client, self._gpio_button.is_pressed)

        self._gpio_button.when_pressed = lambda: self.send_dark_mode_status(
            client, True)
        self._gpio_button.when_released = lambda: self.send_dark_mode_status(
            client, False)

    def send_dark_mode_status(self, client, enabled):
        set_dark_mode = hudiy_api.SetDarkMode()
        set_dark_mode.enabled = enabled
        client.send(hudiy_api.MESSAGE_SET_DARK_MODE, 0,
                    set_dark_mode.SerializeToString())


def main():
    client = Client("dark move gpio example")
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
