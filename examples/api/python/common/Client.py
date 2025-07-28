#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import socket
import struct
import threading
import websocket

import common.Api_pb2 as hudiy_api
from common.Message import Message


class ClientEventHandler:

    def on_hello_response(self, client, message):
        pass

    def on_register_status_icon_response(self, client, message):
        pass

    def on_register_notification_channel_response(self, client, message):
        pass

    def on_register_toast_channel_response(self, client, message):
        pass

    def on_phone_connection_status(self, client, message):
        pass

    def on_phone_levels_status(self, client, message):
        pass

    def on_phone_voice_call_status(self, client, message):
        pass

    def on_navigation_status(self, client, message):
        pass

    def on_navigation_maneuver_details(self, client, message):
        pass

    def on_navigation_maneuver_distance(self, client, message):
        pass

    def on_register_audio_focus_receiver_response(self, client, message):
        pass

    def on_audio_focus_change_response(self, client, message):
        pass

    def on_audio_focus_action(self, client, message):
        pass

    def on_audio_focus_media_key(self, client, message):
        pass

    def on_media_status(self, client, message):
        pass

    def on_media_metadata(self, client, message):
        pass

    def on_projection_status(self, client, message):
        pass

    def on_obd_connection_status(self, client, message):
        pass

    def on_temperature_status(self, client, message):
        pass

    def on_register_action_response(self, client, message):
        pass

    def on_dispatch_action(self, client, message):
        pass

    def on_query_obd_device_response(self, client, message):
        pass

    def on_coverart_request(self, client, message):
        pass


class Client:

    def __init__(self, name):
        self._name = name
        self._socket = None
        self._websocket = None
        self._use_websocket = False
        self._connected = False
        self._event_handler = None
        self._send_lock = threading.Lock()
        self._receive_lock = threading.Lock()
        self._receive_buffer = b''

    def set_event_handler(self, event_handler):
        self._event_handler = event_handler

    def connect(self, hostname, port, use_websocket=False):
        self._use_websocket = use_websocket

        if self._connected:
            self.disconnect()

        if self._use_websocket:
            self._websocket = websocket.create_connection(
                f"ws://{hostname}:{port}/")
            self._socket = None
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((hostname, port))
            self._websocket = None

        self._connected = True
        self._send_hello(self._name)

    def disconnect(self):
        if not self._connected:
            return

        self.send(hudiy_api.MESSAGE_BYEBYE, 0, bytes())

        if self._use_websocket and self._websocket:
            self._websocket.close()
        elif self._socket:
            self._socket.close()

        self._connected = False

    def send(self, id, flags, payload):
        with self._send_lock:
            header = struct.pack('<III', len(payload), id, flags)
            message = header + payload

            if self._use_websocket:
                self._websocket.send_binary(message)
            else:
                self._socket.sendall(message)

    def receive(self) -> Message:
        with self._receive_lock:
            header_size = 12
            header_data = self._receive_exact(header_size)
            (payload_size, id,
             flags) = struct.unpack('<III', header_data[:header_size])
            payload = self._receive_exact(payload_size)
            return Message(id, flags, payload)

    def _receive_exact(self, size):
        data = b''

        while len(data) < size:
            if self._use_websocket:
                if self._receive_buffer:
                    take = min(size - len(data), len(self._receive_buffer))
                    data += self._receive_buffer[:take]
                    self._receive_buffer = self._receive_buffer[take:]
                    continue

                chunk = self._websocket.recv()
                if isinstance(chunk, str):
                    chunk = chunk.encode('utf-8')
                self._receive_buffer += chunk
            else:
                chunk = self._socket.recv(size - len(data))
                if not chunk:
                    raise ConnectionError("Socket closed")
                data += chunk

        return data

    def _send_hello(self, name):
        hello_request = hudiy_api.HelloRequest()
        hello_request.name = name
        hello_request.api_version.major = hudiy_api.API_MAJOR_VERSION
        hello_request.api_version.minor = hudiy_api.API_MINOR_VERSION

        self.send(hudiy_api.MESSAGE_HELLO_REQUEST, 0,
                  hello_request.SerializeToString())

    def wait_for_message(self):
        can_continue = True
        message = self.receive()

        if message.id == hudiy_api.MESSAGE_PING:
            self.send(hudiy_api.MESSAGE_PONG, 0, bytes())
        elif message.id == hudiy_api.MESSAGE_BYEBYE:
            can_continue = False

        if self._event_handler is not None:
            if message.id == hudiy_api.MESSAGE_HELLO_RESPONSE:
                hello_response = hudiy_api.HelloResponse()
                hello_response.ParseFromString(message.payload)
                self._event_handler.on_hello_response(self, hello_response)
            elif message.id == hudiy_api.MESSAGE_REGISTER_STATUS_ICON_RESPONSE:
                resp = hudiy_api.RegisterStatusIconResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_register_status_icon_response(
                    self, resp)
            elif message.id == hudiy_api.MESSAGE_REGISTER_NOTIFICATION_CHANNEL_RESPONSE:
                resp = hudiy_api.RegisterNotificationChannelResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_register_notification_channel_response(
                    self, resp)
            elif message.id == hudiy_api.MESSAGE_REGISTER_TOAST_CHANNEL_RESPONSE:
                resp = hudiy_api.RegisterToastChannelResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_register_toast_channel_response(
                    self, resp)
            elif message.id == hudiy_api.MESSAGE_PHONE_CONNECTION_STATUS:
                resp = hudiy_api.PhoneConnectionStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_phone_connection_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_PHONE_LEVELS_STATUS:
                resp = hudiy_api.PhoneLevelsStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_phone_levels_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_PHONE_VOICE_CALL_STATUS:
                resp = hudiy_api.PhoneVoiceCallStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_phone_voice_call_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_NAVIGATION_STATUS:
                resp = hudiy_api.NavigationStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_navigation_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_NAVIGATION_MANEUVER_DETAILS:
                resp = hudiy_api.NavigationManeuverDetails()
                resp.ParseFromString(message.payload)
                self._event_handler.on_navigation_maneuver_details(self, resp)
            elif message.id == hudiy_api.MESSAGE_NAVIGATION_MANEUVER_DISTANCE:
                resp = hudiy_api.NavigationManeuverDistance()
                resp.ParseFromString(message.payload)
                self._event_handler.on_navigation_maneuver_distance(self, resp)
            elif message.id == hudiy_api.MESSAGE_REGISTER_AUDIO_FOCUS_RECEIVER_RESPONSE:
                resp = hudiy_api.RegisterAudioFocusReceiverResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_register_audio_focus_receiver_response(
                    self, resp)
            elif message.id == hudiy_api.MESSAGE_AUDIO_FOCUS_CHANGE_RESPONSE:
                resp = hudiy_api.AudioFocusChangeResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_change_response(self, resp)
            elif message.id == hudiy_api.MESSAGE_AUDIO_FOCUS_ACTION:
                resp = hudiy_api.AudioFocusAction()
                resp.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_action(self, resp)
            elif message.id == hudiy_api.MESSAGE_AUDIO_FOCUS_MEDIA_KEY:
                resp = hudiy_api.AudioFocusMediaKey()
                resp.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_media_key(self, resp)
            elif message.id == hudiy_api.MESSAGE_MEDIA_STATUS:
                resp = hudiy_api.MediaStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_media_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_MEDIA_METADATA:
                resp = hudiy_api.MediaMetadata()
                resp.ParseFromString(message.payload)
                self._event_handler.on_media_metadata(self, resp)
            elif message.id == hudiy_api.MESSAGE_PROJECTION_STATUS:
                resp = hudiy_api.ProjectionStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_projection_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_OBD_CONNECTION_STATUS:
                resp = hudiy_api.ObdConnectionStatus()
                resp.ParseFromString(message.payload)
                self._event_handler.on_obd_connection_status(self, resp)
            elif message.id == hudiy_api.MESSAGE_REGISTER_ACTION_RESPONSE:
                resp = hudiy_api.RegisterActionResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_register_action_response(self, resp)
            elif message.id == hudiy_api.MESSAGE_DISPATCH_ACTION:
                resp = hudiy_api.DispatchAction()
                resp.ParseFromString(message.payload)
                self._event_handler.on_dispatch_action(self, resp)
            elif message.id == hudiy_api.MESSAGE_QUERY_OBD_DEVICE_RESPONSE:
                resp = hudiy_api.QueryObdDeviceResponse()
                resp.ParseFromString(message.payload)
                self._event_handler.on_query_obd_device_response(self, resp)
            elif message.id == hudiy_api.MESSAGE_COVERART_REQUEST:
                resp = hudiy_api.CoverartRequest()
                resp.ParseFromString(message.payload)
                self._event_handler.on_coverart_request(self, resp)

        return can_continue
