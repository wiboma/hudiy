import common.Api_pb2 as hudiy_api
import time
from common.Client import Client, ClientEventHandler
from gpiozero import Button, RotaryEncoder


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._encoder_button = Button(22, bounce_time=0.1)
        self._encoder = RotaryEncoder(a=17, b=27, max_steps=0)

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self._encoder_button.when_pressed = lambda: self.send_dispatch_action(
            client, "toggle_output_muted")
        self._encoder.when_rotated_clockwise = lambda: self.send_dispatch_action(
            client, "output_volume_down")
        self._encoder.when_rotated_counter_clockwise = lambda: self.send_dispatch_action(
            client, "output_volume_up")

    def send_dispatch_action(self, client, action_name):
        dispatch_action = hudiy_api.DispatchAction()
        dispatch_action.action = action_name
        client.send(hudiy_api.MESSAGE_DISPATCH_ACTION, 0,
                    dispatch_action.SerializeToString())


def main():
    client = Client("volume gpio example")
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

    client.disconnect()


if __name__ == "__main__":
    main()
