from __future__ import annotations

import json
from multiprocessing import resource_tracker, shared_memory
import socket
import struct
import time
from typing import Any, Tuple

DEFAULT_SOCKET_PATH = "/tmp/hudiy_raw_radio.sock"
DEFAULT_SHM_NAME = "HudiyRawRadioData"

FREQUENCY_HZ = 100_100_000
SAMPLE_RATE = 2_048_000
AUTO_GAIN = False
GAIN_TENTHS_DB = 300


class RawRadioClient:

    def __init__(
        self,
        socket_path: str = DEFAULT_SOCKET_PATH,
        shm_name: str = DEFAULT_SHM_NAME,
    ) -> None:
        self.socket_path = socket_path
        self.shm_name = shm_name
        self._sock: socket.socket | None = None
        self._shm: shared_memory.SharedMemory | None = None
        self.is_receiving = False

    def connect(self, retry_interval: float = 1.0) -> None:
        print(f"Connecting to {self.socket_path}")
        while True:
            try:
                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.connect(self.socket_path)
            except (FileNotFoundError, ConnectionRefusedError):
                self._close_sock()
                time.sleep(retry_interval)
                continue
            except Exception as e:
                self._close_sock()
                print(f"Connect error: {e}")
                time.sleep(retry_interval)
                continue

            try:
                self._shm = shared_memory.SharedMemory(name=self.shm_name)
                # !! IMPORTANT !! Unregister from resource_tracker to avoid unlinking shared memory on exit. !! IMPORTANT !!
                try:
                    resource_tracker.unregister(self._shm._name,
                                                "shared_memory")
                except Exception:
                    pass
                print(
                    f"Connected to {self.socket_path}, shm: {self.shm_name}"
                )
                return
            except FileNotFoundError:
                self._close_sock()
                print(
                    f"{self.shm_name} does not exist"
                )
                time.sleep(retry_interval)
            except Exception as e:
                self._close_sock()
                print(f"shm attachment error: {e}")
                time.sleep(retry_interval)

    def send_message(self,
                     name: str,
                     payload: dict[str, Any] | None = None) -> None:
        if not self._sock:
            raise RuntimeError("Not connected")
        payload_str = json.dumps(payload) if payload else ""
        msg = {
            "name": name,
            "payload": payload_str,
            "payloadSize": len(payload_str),
        }
        encoded = json.dumps(msg).encode("utf-8")
        self._sock.sendall(struct.pack("<I", len(encoded)) + encoded)

    def recv_message(self) -> Tuple[str | None, dict[str, Any]]:
        if not self._sock:
            return None, {}
        header = self._sock.recv(4)
        if not header:
            return None, {}
        (length, ) = struct.unpack("<I", header)

        data = bytearray()
        while len(data) < length:
            chunk = self._sock.recv(length - len(data))
            if not chunk:
                return None, {}
            data.extend(chunk)

        msg = json.loads(data.decode("utf-8"))
        payload = json.loads(msg["payload"]) if msg.get("payload") else {}
        return msg.get("name"), payload

    def set_frequency(self, frequency_hz: int) -> None:
        self.send_message("SetFrequency", {"frequency": frequency_hz})

    def set_sample_rate(self, sample_rate: int) -> None:
        self.send_message("SetSampleRate", {"sampleRate": sample_rate})

    def set_gain(self,
                 auto_gain: bool = False,
                 gain_tenths_db: int = 300) -> None:
        self.send_message("SetGain", {
            "autoGain": auto_gain,
            "gain": gain_tenths_db
        })

    def start_reception(self) -> None:
        self.send_message("StartReception")

    def stop_reception(self) -> None:
        if self.is_receiving:
            self.send_message("StopReception")
            self.is_receiving = False

    def close(self) -> None:
        try:
            self.stop_reception()
            self.send_message("Quit")
        except Exception:
            pass
        self._close_sock()
        self._close_shm()

    def _close_sock(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def _close_shm(self) -> None:
        if self._shm:
            try:
                self._shm.close()
            except Exception:
                pass
            self._shm = None

    def __enter__(self) -> RawRadioClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


def main() -> None:
    client = RawRadioClient()
    try:
        client.connect()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return

    total_bytes = 0

    with client:
        client.set_frequency(FREQUENCY_HZ)
        client.set_sample_rate(SAMPLE_RATE)
        client.set_gain(auto_gain=AUTO_GAIN, gain_tenths_db=GAIN_TENTHS_DB)
        client.start_reception()
        print(
            f"Starting reception: {FREQUENCY_HZ} Hz, {SAMPLE_RATE} S/s"
        )

        try:
            while True:
                name, payload = client.recv_message()
                if not name:
                    print("\nConnection closed by handler.")
                    break

                if name == "RawDataProduced":
                    size = payload.get("size", 0)
                    if client._shm and size > 0:
                        view = client._shm.buf[:size]
                        total_bytes += size
                        print(
                            f"\rReceived: {total_bytes} B, chunk: {size} B",
                            end="",
                            flush=True,
                        )

                        # !! IMPORTANT !! Acknowledge data consumption. !! IMPORTANT !!
                        client.send_message("RawDataConsumed")
                        view.release()

                elif name == "ReceptionStatusChanged":
                    status = payload.get("status", False)
                    if status:
                        client.is_receiving = True
                        print("\nReception active.")
                    elif client.is_receiving:
                        client.is_receiving = False
                        print("\nReception stopped by handler.")
                        break

                elif name == "FrequencyChanged":
                    freq = payload.get("frequency", 0)
                    print(f"Frequency: {freq} Hz")

                elif name == "SampleRateChanged":
                    rate = payload.get("sampleRate", 0)
                    print(f"Sample rate: {rate} S/s")

                elif name == "GainChanged":
                    auto = payload.get("autoGain", True)
                    gain = payload.get("gain", 0) / 10.0
                    print(f"Gain: {'Auto' if auto else f'{gain:.1f} dB'}")

                elif name == "Ready":
                    print("Handler ready.")

        except KeyboardInterrupt:
            print("\nStopping...")

    print("Disconnected.")


if __name__ == "__main__":
    main()
