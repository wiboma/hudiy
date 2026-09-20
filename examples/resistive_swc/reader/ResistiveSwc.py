#
#  Copyright (C) Hudiy Project - All Rights Reserved
#

import argparse
import threading
import serial
import struct
import time
from dataclasses import dataclass
from typing import Union, Optional

import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler

PORT = '/dev/ttyACM0'
BAUDRATE = 115200

# ADC idle state threshold (max Pico2 with pull-up is 4095 [12 bit unsigned])
ADC_IDLE_THRESHOLD = 4000

# VAL * ADC_POLL_RATE_MS (defined in Pico2 firmware - default 10ms)
PRESS_DEBOUNCE = 2  # * 10ms = 20ms
RELEASE_DEBOUNCE = 2  # * 10ms = 20ms
REPEAT_DELAY = 60  # * 10ms = 600ms
REPEAT_INTERVAL = 30  # * 10ms = 300ms


@dataclass
class ButtonConfig:
    adc_id: int  # ID of the ADC port
    min_val: int  # minimum ADC value
    max_val: int  # maximum ADC value
    value: Union[int,
                 str]  # button code or action to dispatch on key press/release
    autorepeat: bool  # repeatedly dispatch `value` at REPEAT_INTERVAL when held


@dataclass
class AdcState:
    current: Optional[ButtonConfig] = None
    next: Optional[ButtonConfig] = None
    count: int = 0


BUTTON_CONFIG = [
    ButtonConfig(adc_id=1,
                 min_val=0,
                 max_val=35,
                 value=hudiy_api.KeyEvent.KEY_TYPE_TOGGLE_PLAY,
                 autorepeat=False),
    ButtonConfig(adc_id=1,
                 min_val=40,
                 max_val=120,
                 value="output_volume_up",
                 autorepeat=True),
    ButtonConfig(adc_id=1,
                 min_val=220,
                 max_val=290,
                 value=hudiy_api.KeyEvent.KEY_TYPE_NEXT_TRACK,
                 autorepeat=False),
    ButtonConfig(adc_id=1,
                 min_val=450,
                 max_val=540,
                 value="output_volume_down",
                 autorepeat=True),
    ButtonConfig(adc_id=1,
                 min_val=800,
                 max_val=920,
                 value=hudiy_api.KeyEvent.KEY_TYPE_PREVIOUS_TRACK,
                 autorepeat=False),
    ButtonConfig(adc_id=2,
                 min_val=40,
                 max_val=120,
                 value="toggle_output_muted",
                 autorepeat=False),
    ButtonConfig(adc_id=2,
                 min_val=220,
                 max_val=290,
                 value="resume_android_auto_projection",
                 autorepeat=False),
    ButtonConfig(adc_id=2,
                 min_val=450,
                 max_val=540,
                 value=hudiy_api.KeyEvent.KEY_TYPE_HANGUP_CALL,
                 autorepeat=False),
    ButtonConfig(adc_id=2,
                 min_val=800,
                 max_val=920,
                 value="go_home",
                 autorepeat=False),
    ButtonConfig(adc_id=2,
                 min_val=1450,
                 max_val=1550,
                 value=hudiy_api.KeyEvent.KEY_TYPE_ANSWER_CALL,
                 autorepeat=False),
]


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._client = None
        self._running = True

        self._states = {
            adc_id: AdcState()
            for adc_id in set(button.adc_id for button in BUTTON_CONFIG)
        }

        threading.Thread(target=self._adc_read_worker, daemon=True).start()

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, app version: {}.{}, api version: {}.{}"
            .format(message.result, message.app_version.major,
                    message.app_version.minor, message.api_version.major,
                    message.api_version.minor))

        self._client = client

    def _dispatch_key_event(self, key_type, event_type):
        if not self._client: return
        key_event = hudiy_api.KeyEvent()
        key_event.key_type = key_type
        key_event.event_type = event_type
        self._client.send(hudiy_api.MESSAGE_KEY_EVENT, 0,
                          key_event.SerializeToString())

    def _dispatch_action(self, action_name):
        if not self._client: return
        dispatch_action = hudiy_api.DispatchAction()
        dispatch_action.action = action_name
        self._client.send(hudiy_api.MESSAGE_DISPATCH_ACTION, 0,
                          dispatch_action.SerializeToString())

    def _resolve_button(self, message_id, adc_value):
        for button in BUTTON_CONFIG:
            if button.adc_id == message_id and button.min_val <= adc_value <= button.max_val:
                return button
        return None

    def _adc_read_worker(self):
        struct_format = '<BH'
        expected_size = struct.calcsize(struct_format)

        while self._running:
            try:
                with serial.Serial(PORT, BAUDRATE, timeout=1.0) as serial_port:
                    serial_port.dtr = True
                    print(f"listening on {PORT}")
                    buffer = bytearray()

                    while self._running:
                        chunk = serial_port.read(max(1,
                                                     serial_port.in_waiting))
                        if not chunk:
                            continue

                        buffer.extend(chunk)

                        while len(buffer) >= expected_size:
                            message_id, payload = struct.unpack(
                                struct_format, buffer[:expected_size])
                            buffer = buffer[expected_size:]
                            self._handle_adc_data(message_id, payload)

            except (serial.SerialException, OSError) as exception:
                if self._running:
                    print(f"communication error: {exception}. Retrying...")
                    time.sleep(3)

    def _handle_adc_data(self, message_id, payload):
        if message_id not in self._states:
            return

        channel = self._states[message_id]
        current_read_button = self._resolve_button(
            message_id, payload) if payload < ADC_IDLE_THRESHOLD else None

        if current_read_button == channel.next:
            channel.count += 1
            self._handle_autorepeat(channel)
        else:
            channel.next = current_read_button
            channel.count = 1

        target_debounce = RELEASE_DEBOUNCE if channel.next is None else PRESS_DEBOUNCE

        if channel.count == target_debounce:
            if channel.next != channel.current:
                self._handle_button_transition(channel)

    def _handle_autorepeat(self, channel):
        if channel.current is None or not channel.current.autorepeat:
            return

        held_time = channel.count - PRESS_DEBOUNCE
        if held_time >= REPEAT_DELAY and (held_time -
                                          REPEAT_DELAY) % REPEAT_INTERVAL == 0:
            button = channel.current
            if isinstance(button.value, str):
                self._dispatch_action(button.value)
            else:
                self._dispatch_key_event(button.value,
                                         hudiy_api.KeyEvent.EVENT_TYPE_PRESS)

    def _handle_button_transition(self, channel):
        old_button = channel.current
        new_button = channel.next

        if old_button is not None and not isinstance(old_button.value, str):
            self._dispatch_key_event(old_button.value,
                                     hudiy_api.KeyEvent.EVENT_TYPE_RELEASE)

        channel.current = new_button

        if new_button is not None:
            if isinstance(new_button.value, str):
                self._dispatch_action(new_button.value)
            else:
                self._dispatch_key_event(new_button.value,
                                         hudiy_api.KeyEvent.EVENT_TYPE_PRESS)

    def stop(self):
        self._running = False


def run_calibrate():
    print("calibration mode")
    print(
        f"listening on {PORT}. Press and hold SWC button or press CTRL+C to exit.\n"
    )

    struct_format = '<BH'
    expected_size = struct.calcsize(struct_format)

    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1.0) as serial_port:
            serial_port.dtr = True
            buffer = bytearray()

            while True:
                chunk = serial_port.read(max(1, serial_port.in_waiting))
                if not chunk:
                    continue

                buffer.extend(chunk)

                while len(buffer) >= expected_size:
                    message_id, payload = struct.unpack(
                        struct_format, buffer[:expected_size])
                    buffer = buffer[expected_size:]

                    if payload < ADC_IDLE_THRESHOLD:
                        print(f"ADC{message_id} | {payload}")

    except (serial.SerialException, OSError) as exception:
        print(f"communication error: {exception}")


def main():
    parser = argparse.ArgumentParser(description="Hudiy Resistive SWC")
    parser.add_argument(
        '-c',
        '--calibrate',
        action='store_true',
        help="Run in calibration mode and do not connect to Hudiy API")
    arguments = parser.parse_args()

    if arguments.calibrate:
        try:
            run_calibrate()
        except KeyboardInterrupt:
            pass
        return

    client = Client("Hudiy Resistive SWC")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)

    try:
        while True:
            try:
                client.connect('127.0.0.1', 44405)
                while True:
                    if not client.wait_for_message():
                        print("reconnecting...")
                        break
            except (ConnectionError, OSError) as exception:
                print(f"connection error: {exception}. Retrying...")
                time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        event_handler.stop()
        client.disconnect()


if __name__ == "__main__":
    main()
