import logging
import threading
import itertools
import time
from queue import Queue, Empty
from collections import deque
from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS
from jinja2 import TemplateNotFound
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='templates')
CORS(app)

client = Client("Chart")
request_counter = itertools.count(1)
pid_history_capacity = 300
pending_requests = {}
database = {}


def send_obd_query(pid):
    req_id = next(request_counter)
    query = hudiy_api.QueryObdDeviceRequest()
    query.commands[:] = [pid]
    query.request_code = req_id

    try:
        client.send(hudiy_api.MESSAGE_QUERY_OBD_DEVICE_REQUEST, 0,
                    query.SerializeToString())
        return req_id
    except (OSError, BrokenPipeError):
        return None


@app.route('/<page_name>')
def render_page(page_name):
    try:
        return render_template(f'{page_name}.html')
    except TemplateNotFound:
        abort(404)


@app.route('/history', methods=['GET'])
def get_history():
    pid = str(request.args.get('pid', '')).lower()
    data = list(database.get(pid, []))
    return jsonify({"data": data, "maxCapacity": pid_history_capacity})


@app.route('/value', methods=['GET'])
def get_value():
    pid = request.args.get('pid')
    response_queue = Queue()
    req_id = send_obd_query(pid)

    if req_id is None:
        return jsonify({"error": "Hudiy is disconnected"}), 503

    pending_requests[req_id] = response_queue

    try:
        result = response_queue.get(timeout=10)
        return jsonify({"pid": pid, "value": result})
    except Empty:
        return jsonify({"error": "Timeout"}), 504
    finally:
        pending_requests.pop(req_id, None)


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._timer = None

    def on_hello_response(self, client, message):
        subs = hudiy_api.SetStatusSubscriptions()
        subs.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.OBD)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    subs.SerializeToString())

    def on_query_obd_device_response(self, client, message):
        queue = pending_requests.get(message.request_code)
        if not queue:
            return

        parsed_value = None
        if message.result and message.data:
            try:
                data = message.data[0]
                pid_key = f"{(int(data[:2], 16) - 0x40):02x}{data[2:4]}".lower(
                )
                parsed_value = data
                database.setdefault(
                    pid_key,
                    deque(maxlen=pid_history_capacity)).append(parsed_value)
            except Exception:
                pass

        queue.put(parsed_value)

    def on_obd_connection_status(self, client, message):
        if message.state == hudiy_api.ObdConnectionStatus.OBD_CONNECTION_STATE_DISCONNECTED:
            database.clear()

    def get_timer(self):
        return self._timer


def run_api():
    app.run(host='0.0.0.0', port=44411, debug=False, use_reloader=False)


def main():
    threading.Thread(target=run_api, daemon=True).start()
    client.set_event_handler(EventHandler())

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


if __name__ == '__main__':
    main()
