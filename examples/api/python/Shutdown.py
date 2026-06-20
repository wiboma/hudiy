#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import subprocess
import math
import time
import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._shutdown_delay_minutes = 10
        self._notify_at_minutes = [9, 7, 5, 3, 1]
        self._action_reset = "reset_shutdown"

        self._notification_channel_id = None
        self._icon_id = None
        self._toast_channel_id = None
        self._is_disconnected_state = False
        self._client = None

        self._shutdown_thread = None
        self._cancel_event = threading.Event()

    def reset(self):
        self.stop_shutdown_sequence()
        self._notification_channel_id = None
        self._icon_id = None
        self._is_disconnected_state = False
        self._client = None

    def set_icon_visibility(self, visible):
        if self._icon_id is None or self._client is None:
            return

        change_status_icon_state = hudiy_api.ChangeStatusIconState()
        change_status_icon_state.id = self._icon_id
        change_status_icon_state.visible = visible
        self._client.send(hudiy_api.MESSAGE_CHANGE_STATUS_ICON_STATE, 0,
                          change_status_icon_state.SerializeToString())

    def show_notification(self, minutes_left):
        if self._notification_channel_id is None or self._client is None:
            return

        show_notification = hudiy_api.ShowNotification()
        show_notification.channel_id = self._notification_channel_id
        show_notification.title = "Shutdown Timer"
        show_notification.description = f"Shutdown will be performed in {minutes_left} minute(s)"
        show_notification.icon_font_family = "Material Symbols Rounded"
        show_notification.icon_name = "power_settings_new"
        show_notification.action = self._action_reset
        show_notification.play_sound = True

        self._client.send(hudiy_api.MESSAGE_SHOW_NOTIFICATION, 0,
                          show_notification.SerializeToString())

    def show_toast(self):
        if self._toast_channel_id is None or self._client is None:
            return

        show_toast = hudiy_api.ShowToast()
        show_toast.channel_id = self._toast_channel_id
        show_toast.message = "Shutdown timer reset"
        show_toast.icon_font_family = "Material Symbols Rounded"
        show_toast.icon_name = "power_settings_new"

        self._client.send(hudiy_api.MESSAGE_SHOW_TOAST, 0,
                          show_toast.SerializeToString())

    def _shutdown_worker(self):
        total_seconds = int(self._shutdown_delay_minutes * 60)

        notify_targets = {int(m * 60) for m in self._notify_at_minutes}

        while total_seconds >= 0:
            if total_seconds in notify_targets:
                minutes_left = math.ceil(total_seconds / 60.0)
                self.show_notification(minutes_left)

            if total_seconds == 0:
                subprocess.run(["systemctl", "poweroff"])
                return

            if self._cancel_event.wait(1.0):
                return

            total_seconds -= 1

    def start_shutdown_sequence(self):
        self._cancel_event.clear()
        self.set_icon_visibility(True)

        self._shutdown_thread = threading.Thread(target=self._shutdown_worker)
        self._shutdown_thread.start()

    def stop_shutdown_sequence(self):
        self._cancel_event.set()
        if self._shutdown_thread is not None:
            self._shutdown_thread.join(timeout=2.0)
            self._shutdown_thread = None

        self.set_icon_visibility(False)

    def on_hello_response(self, client, message):
        self._client = client

        set_status_subscriptions = hudiy_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.PHONE)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

        register_notification_channel_request = hudiy_api.RegisterNotificationChannelRequest(
        )
        register_notification_channel_request.name = "Shutdown Notifications"
        register_notification_channel_request.description = "Notifies about pending automatic system shutdown"
        client.send(hudiy_api.MESSAGE_REGISTER_NOTIFICATION_CHANNEL_REQUEST, 0,
                    register_notification_channel_request.SerializeToString())

        register_toast_channel_request = hudiy_api.RegisterToastChannelRequest(
        )
        register_toast_channel_request.name = "Shutdown Toast"
        register_toast_channel_request.description = "Toasts about pending automatic system shutdown"

        client.send(hudiy_api.MESSAGE_REGISTER_TOAST_CHANNEL_REQUEST, 0,
                    register_toast_channel_request.SerializeToString())

        register_status_icon_request = hudiy_api.RegisterStatusIconRequest()
        register_status_icon_request.description = "Shutdown pending"
        register_status_icon_request.icon_name = "power_settings_new"
        register_status_icon_request.icon_font_family = "Material Symbols Rounded"
        client.send(hudiy_api.MESSAGE_REGISTER_STATUS_ICON_REQUEST, 0,
                    register_status_icon_request.SerializeToString())

        register_action_request = hudiy_api.RegisterActionRequest()
        register_action_request.action = self._action_reset
        client.send(hudiy_api.MESSAGE_REGISTER_ACTION_REQUEST, 0,
                    register_action_request.SerializeToString())

    def on_register_notification_channel_response(self, client, message):
        if message.result == hudiy_api.RegisterNotificationChannelResponse.REGISTER_NOTIFICATION_CHANNEL_RESULT_OK:
            self._notification_channel_id = message.id

    def on_register_toast_channel_response(self, client, message):
        if message.result == hudiy_api.RegisterToastChannelResponse.REGISTER_TOAST_CHANNEL_RESULT_OK:
            self._toast_channel_id = message.id

    def on_register_status_icon_response(self, client, message):
        if message.result == hudiy_api.RegisterStatusIconResponse.REGISTER_STATUS_ICON_RESULT_OK:
            self._icon_id = message.id
            if self._shutdown_thread is not None and self._shutdown_thread.is_alive(
            ):
                self.set_icon_visibility(True)

    def on_phone_connection_status(self, client, message):
        is_disconnected = (message.state == hudiy_api.PhoneConnectionStatus.
                           PHONE_CONNECTION_STATE_DISCONNECTED)
        is_connected = (message.state == hudiy_api.PhoneConnectionStatus.
                        PHONE_CONNECTION_STATE_CONNECTED)

        if is_disconnected and not self._is_disconnected_state:
            self._is_disconnected_state = True
            self.stop_shutdown_sequence()
            self.start_shutdown_sequence()
        elif is_connected and self._is_disconnected_state:
            self._is_disconnected_state = False
            self.stop_shutdown_sequence()

    def on_dispatch_action(self, client, message):
        if message.action == self._action_reset:
            if self._is_disconnected_state:
                self.stop_shutdown_sequence()
                self.start_shutdown_sequence()
                self.show_toast()


def main():
    client = Client("auto shutdown script")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)

    try:
        while True:
            try:
                client.connect('127.0.0.1', 44405)
                while True:
                    if not client.wait_for_message():
                        break
            except Exception as e:
                print(f"Error: {e}")
                pass

            event_handler.reset()
            time.sleep(2)

    except KeyboardInterrupt:
        pass
    finally:
        event_handler.reset()
        client.disconnect()


if __name__ == "__main__":
    main()
