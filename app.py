import os

from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello world'

@app.route('/incoming-call')
def incoming_call():
    app_url = request.base_url.rsplit('/', 1)[0] + '/'

    resp = VoiceResponse()
    prompt_url = app_url + url_for('static', filename='prompts/sample.mp3')
    resp.play(prompt_url)

    with resp.gather(numDigits=1, action='/handle-key', method='POST') as g:
        g.say('When you\'re ready, press 1.')

    return str(resp)

@app.route('/handle-key')
def handle_key():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = VoiceResponse()
        resp.record(maxLength='30', action='/handle-recording')
        return str(resp)

@app.route('/handle-recording', methods=['GET', 'POST'])
def handle_recording():
    resp = VoiceResponse()
    recording_url = request.values.get("RecordingUrl", None)
    print recording_url
    resp.say("Thanks! Goodbye.")
    return str(resp)

if __name__ == '__main__':
    app.run()
