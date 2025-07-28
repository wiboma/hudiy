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

        set_status_subscriptions = hudiy_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.NAVIGATION)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

    def on_navigation_status(self, client, message):
        print("navigation status: {}, source {}".format(
            message.state, message.source))

    def on_navigation_maneuver_details(self, client, message):
        print(
            "navigation maneuver details, description: {}, icon size: {}, side: {}, type: {}, angle: {}"
            .format(message.description, len(message.icon),
                    message.maneuver_side, message.maneuver_type,
                    message.maneuver_angle))

    def on_navigation_maneuver_distance(self, client, message):
        print("navigation maneuver distance, label: {}".format(message.label))


def main():
    client = Client("navigation status example")
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
