# Description

This directory contains an example Python client for receiving I/Q samples from Hudiy's `radio_handler` component. This example can be used as a starting point for building custom SDR applications such as HD Radio. See also the audio focus examples to integrate audio playback with Hudiy.

## Communication

- **UNIX Domain Socket (`/tmp/hudiy_raw_radio.sock`)**  
  Handles control messages.

- **Shared Memory (`/dev/shm/HudiyRawRadioData`)**  
  Used to stream I/Q samples from the handler.

### Frame format

| Field | Type | Description |
|---|---|---|
| **Size** | 32-bit unsigned integer (little-endian) | Length (in bytes) of the JSON message |
| **Message** | `n` bytes | UTF-8 JSON |

The JSON message structure:

```json
{
  "name": "Name of the message",
  "payload": "Payload of the message",
  "payloadSize": Size of the message payload
}
```

### Messages

| Message | Direction | Parameters | Description |
|---|---|---|---|
| `Ready` | Handler &rarr; Client | _None_ | Sent when the connection is established and the handler is ready |
| `SetFrequency` | Client &rarr; Handler | `frequency` (Hz) | Sets the center frequency |
| `FrequencyChanged` | Handler &rarr; Client | `frequency` (Hz) | Confirms the current center frequency |
| `SetSampleRate` | Client &rarr; Handler | `sampleRate` | Sets the sampling rate |
| `SampleRateChanged` | Handler &rarr; Client | `sampleRate` | Confirms the current sampling rate |
| `SetGain` | Client &rarr; Handler | `autoGain` (bool)<br>`gain` (int32) | Sets manual gain in tenths of dB or enables/disables auto gain |
| `GainChanged` | Handler &rarr; Client | `autoGain` (bool)<br>`gain` (int32) | Confirms the current gain settings |
| `StartReception` | Client &rarr; Handler | _None_ | Starts streaming |
| `StopReception` | Client &rarr; Handler | _None_ | Stops streaming |
| `ReceptionStatusChanged` | Handler &rarr; Client | `status` (bool) | Current streaming state (`true` = started, `false` = stopped) |
| `RawDataProduced` | Handler &rarr; Client | `size` (bytes) | Signals that a new chunk of `size` bytes is ready in shared memory |
| `RawDataConsumed` | Client &rarr; Handler | _None_ | Confirms the chunk in shared memory was processed, releasing the buffer for the next write |
| `Quit` | Client &rarr; Handler | _None_ | Closes the session |

### Shared Memory Buffer

- **Path:** `/dev/shm/HudiyRawRadioData`
- **Size:** 256 KB

### I/Q Samples

Samples in shared memory are 8-bit unsigned integers interleaved as in-phase (I) and quadrature (Q) pairs.

## How to use

```bash
python3 raw_radio_client.py
```
