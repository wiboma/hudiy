#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._timer = None
        self._request_code = 0

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        set_status_subscriptions = hudiy_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.OBD)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

        self.query_obd_device(client)

    def on_obd_connection_status(self, client, message):
        print("obd connection status, state: {}".format(message.state))

    def on_query_obd_device_response(self, client, message):
        print(
            f"on query obd device response, result {message.result}, data: {message.data}, request code: {message.request_code}"
        )

        if message.result:
            # E. g. 410D74
            hex_value = message.data[0][4] + message.data[0][5]
            speed_kph = int(hex_value, 16)
            print(f"speed {speed_kph}km/h")

    def query_obd_device(self, client):
        query_obd_device = hudiy_api.QueryObdDeviceRequest()
        query_obd_device.commands[:] = ["010D"]
        self._request_code += 1
        query_obd_device.request_code = self._request_code
        client.send(hudiy_api.MESSAGE_QUERY_OBD_DEVICE_REQUEST, 0,
                    query_obd_device.SerializeToString())

        self._timer = threading.Timer(0.01, self.query_obd_device, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("obd read example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    if event_handler.get_timer() is not None:
        event_handler.get_timer().cancel()

    client.disconnect()


if __name__ == "__main__":
    main()
