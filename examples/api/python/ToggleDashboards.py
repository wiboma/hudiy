import itertools
import time
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._action = "toggle_dashboards"

        # Dashboards to toggle - actions from dashboards.json
        self._actions = [
            "hudiy_dashboard", "obd_charts", "obd_blocks", "obd_combined"
        ]
        self._actions_iterator = itertools.cycle(self._actions)
        next(self._actions_iterator)

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_action_request = hudiy_api.RegisterActionRequest()
        register_action_request.action = self._action

        client.send(hudiy_api.MESSAGE_REGISTER_ACTION_REQUEST, 0,
                    register_action_request.SerializeToString())

    def on_register_action_response(self, client, message):
        print("register action response, result: {}, action: {}".format(
            message.result, message.action))

        if message.result:
            print("action successfully registered")

    def on_dispatch_action(self, client, message):
        print("dispatch action, action: {}".format(message.action))

        if message.action == self._action:
            self.toggle_dashboard(client)

    def toggle_dashboard(self, client):
        next_dashboard = next(self._actions_iterator)

        dispatch_action = hudiy_api.DispatchAction()
        dispatch_action.action = next_dashboard

        client.send(hudiy_api.MESSAGE_DISPATCH_ACTION, 0,
                    dispatch_action.SerializeToString())

        print("toggle dashboard: {}".format(dispatch_action.action))


def main():
    client = Client("dashboard toggle")
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
