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

        self._gpio_button.when_pressed = lambda: self.send_reverse_camera_status(
            client, True)
        self._gpio_button.when_released = lambda: self.send_reverse_camera_status(
            client, False)

    def send_reverse_camera_status(self, client, visible):
        set_reverse_camera_status = hudiy_api.SetReverseCameraStatus()
        set_reverse_camera_status.visible = visible
        client.send(hudiy_api.MESSAGE_SET_REVERSE_CAMERA_STATUS, 0,
                    set_reverse_camera_status.SerializeToString())


def main():
    client = Client("reverse camera gpio example")
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
