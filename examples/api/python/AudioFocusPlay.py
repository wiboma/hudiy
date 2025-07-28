#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import threading
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._id = 0

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_audio_focus_receiver_request = hudiy_api.RegisterAudioFocusReceiverRequest(
        )
        register_audio_focus_receiver_request.name = "audio focus example"
        register_audio_focus_receiver_request.duck_priority = -1
        register_audio_focus_receiver_request.category = hudiy_api.RegisterAudioFocusReceiverRequest.AUDIO_STREAM_CATEGORY_ENTERTAINMENT
        client.send(hudiy_api.MESSAGE_REGISTER_AUDIO_FOCUS_RECEIVER_REQUEST, 0,
                    register_audio_focus_receiver_request.SerializeToString())

    def on_register_audio_focus_receiver_response(self, client, message):
        print("register audio focus receiver response, result: {}, id: {}".
              format(message.result, message.id))
        self._id = message.id

        audio_focus_change_request = hudiy_api.AudioFocusChangeRequest()
        audio_focus_change_request.id = self._id
        audio_focus_change_request.type = hudiy_api.AudioFocusChangeRequest.AUDIO_FOCUS_TYPE_GAIN

        client.send(hudiy_api.MESSAGE_AUDIO_FOCUS_CHANGE_REQUEST, 0,
                    audio_focus_change_request.SerializeToString())

    def on_audio_focus_change_response(self, client, message):
        print("audio focus change response, result: {}, id: {}".format(
            message.result, message.id))

    def on_audio_focus_action(self, client, message):
        action = message.action

        if action == hudiy_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_SUSPEND:
            print("suspend audio stream")
        elif action == hudiy_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_RESTORE:
            print("resume audio stream")
        elif action == hudiy_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_LOSS:
            print("stop audio stream, lost focus type: {}".format(
                message.lost_type))
        elif action == hudiy_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_DUCK_START:
            print("decrease stream volume")
        elif action == hudiy_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_DUCK_END:
            print("restore stream volume")

    def on_audio_focus_media_key(self, client, message):
        event_type = message.event_type
        key_type = message.key_type

        if key_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PLAY:
            if event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("play pressed")
            elif event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("play released")
        elif key_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PAUSE:
            if event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("pause pressed")
            elif event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("pause released")
        elif key_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PREVIOUS:
            if event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("previous pressed")
            elif event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("previous released")
        elif key_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_NEXT:
            if event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("next pressed")
            elif event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("next released")
        elif key_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_TOGGLE_PLAY:
            if event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("toggle play pressed")
            elif event_type == hudiy_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("toggle play released")

    def get_audio_focus_receiver_id(self):
        return self._id


def main():
    client = Client("audio focus duck")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    if event_handler.get_audio_focus_receiver_id() is not None:
        unregister_audio_focus_receiver = hudiy_api.UnregisterAudioFocusReceiver(
        )
        unregister_audio_focus_receiver.id = event_handler.get_audio_focus_receiver_id(
        )
        client.send(hudiy_api.MESSAGE_UNREGISTER_AUDIO_FOCUS_RECEIVER, 0,
                    unregister_audio_focus_receiver.SerializeToString())

    client.disconnect()


if __name__ == "__main__":
    main()
