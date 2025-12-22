import logging
import threading
import time
from flask import Flask, render_template, abort
from flask_cors import CORS
from jinja2 import TemplateNotFound
import common.Api_pb2 as hudiy_api
from common.Client import Client, ClientEventHandler

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__, template_folder='templates')
CORS(app)
client = Client("Chart")
show_action_name = "show_idle_overlay"
overlay_name = "idle_overlay"


def set_overlay_visibility(client, visibility):
    set_custom_overlay_visibility = hudiy_api.SetCustomOverlayVisibility()
    set_custom_overlay_visibility.identifier = overlay_name
    set_custom_overlay_visibility.visibility = visibility
    client.send(hudiy_api.MESSAGE_SET_CUSTOM_OVERLAY_VISIBILITY, 0,
                set_custom_overlay_visibility.SerializeToString())


def hide_overlay(client):
    set_overlay_visibility(client, hudiy_api.OVERLAY_VISIBILITY_NONE)


def show_overlay(client):
    set_overlay_visibility(client, hudiy_api.OVERLAY_VISIBILITY_ALWAYS)


@app.route('/idle')
def render_page():
    try:
        return render_template(f'idle.html')
    except TemplateNotFound:
        abort(404)


@app.route('/hide')
def hide():
    hide_overlay(client)
    return "", 200


class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        register_action_request = hudiy_api.RegisterActionRequest()
        register_action_request.action = show_action_name
        client.send(hudiy_api.MESSAGE_REGISTER_ACTION_REQUEST, 0,
                    register_action_request.SerializeToString())

        subs = hudiy_api.SetStatusSubscriptions()
        subs.subscriptions.append(
            hudiy_api.SetStatusSubscriptions.Subscription.PHONE)
        client.send(hudiy_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    subs.SerializeToString())

    def on_phone_voice_call_status(self, client, message):
        if message.state == hudiy_api.PhoneVoiceCallStatus.PHONE_VOICE_CALL_STATE_INCOMING:
            hide_overlay(client)

    def on_register_action_response(self, client, message):
        print("register action response, result: {}, action: {}".format(
            message.result, message.action))

    def on_dispatch_action(self, client, message):
        if message.action == show_action_name:
            show_overlay(client)


def run_api():
    app.run(host='0.0.0.0', port=44412, debug=False, use_reloader=False)


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
