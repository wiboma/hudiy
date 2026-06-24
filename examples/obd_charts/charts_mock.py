import logging
import threading
import time
import random
from collections import deque
from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS
from jinja2 import TemplateNotFound

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='templates')
CORS(app)

pid_history_capacity = 300
database = {}

SUPPORTED_PIDS = ['0104', '0105', '010f', '010c', '010d', '0111']


def get_obd_hex_frame(pid):
    pid = pid.lower()

    # ELM327 Format: [41 (Mode 1 Response)] [PID (2 chars)] [Data Bytes (2-4 chars)]

    if pid == '0104':  # Engine Load (0 - 100%)
        # JS Formula: (A * 100) / 255. Reversing: A = Load * 255 / 100
        mock_load = random.randint(15, 95)
        byte_a = int((mock_load * 255) / 100)
        return f"4104{byte_a:02x}"

    elif pid == '0105':  # Coolant Temp (-40 to 215C)
        # JS Formula: A - 40. Reversing: A = Temp + 40
        mock_temp = random.randint(80, 105)
        byte_a = mock_temp + 40
        return f"4105{byte_a:02x}"

    elif pid == '010f':  # Intake Air Temp (-40 to 215C)
        # JS Formula: A - 40. Reversing: A = Temp + 40
        mock_temp = random.randint(20, 45)
        byte_a = mock_temp + 40
        return f"410f{byte_a:02x}"

    elif pid == '010c':  # Engine RPM
        # JS Formula: ((A * 256) + B) / 4. Reversing: (A*256 + B) = RPM * 4
        mock_rpm = random.randint(800, 2400)
        raw_val = mock_rpm * 4
        byte_a = (raw_val >> 8) & 0xFF
        byte_b = raw_val & 0xFF
        return f"410c{byte_a:02x}{byte_b:02x}"

    elif pid == '010d':  # Vehicle Speed (0 - 255 km/h)
        # JS Formula: A. Reversing: A = Speed
        mock_speed = random.randint(0, 140)
        byte_a = mock_speed
        return f"410d{byte_a:02x}"

    elif pid == '0111':  # Throttle Position (0 - 100%)
        # JS Formula: (A * 100) / 255. Reversing: A = Throttle * 255 / 100
        mock_throttle = random.randint(5, 100)
        byte_a = int((mock_throttle * 255) / 100)
        return f"4111{byte_a:02x}"

    else:
        pid_hex = pid[2:4] if len(pid) == 4 else '00'
        return f"41{pid_hex}00"


def generate_mock_data():
    while True:
        for pid in SUPPORTED_PIDS:
            hex_frame = get_obd_hex_frame(pid)
            database.setdefault(
                pid, deque(maxlen=pid_history_capacity)).append(hex_frame)

        time.sleep(1)


@app.route('/<path:page_name>')
def render_page(page_name):
    try:
        return render_template(f'{page_name}.html')
    except TemplateNotFound:
        abort(404)


@app.route('/history', methods=['GET'])
def get_history():
    pid_arg = request.args.get('pid')
    if not pid_arg:
        return jsonify({"error": "Missing 'pid' parameter in request"}), 400

    pid = str(pid_arg).lower()
    data = list(database.get(pid, []))

    return jsonify({"data": data, "maxCapacity": pid_history_capacity})


@app.route('/value', methods=['GET'])
def get_value():
    pid_arg = request.args.get('pid')
    if not pid_arg:
        return jsonify({"error": "Missing 'pid' parameter in request"}), 400

    pid = str(pid_arg).lower()
    history = database.get(pid, [])

    if history:
        latest_value = history[-1]
        return jsonify({"pid": pid, "value": latest_value})
    else:
        return jsonify({"error": f"Data not available yet for PID {pid}"}), 503


def main():
    generator_thread = threading.Thread(target=generate_mock_data, daemon=True)
    generator_thread.start()

    app.run(host='0.0.0.0', port=44411, debug=False, use_reloader=False)


if __name__ == '__main__':
    main()
