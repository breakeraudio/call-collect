import os

from flask import Flask, request, redirect, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello world'

@app.route('/incoming-call')
def incoming_call():
    app_url = request.base_url.rsplit('/', 1)[0]

    resp = VoiceResponse()
    prompt_url = app_url + url_for('static', filename='prompts/sample.mp3')
    resp.play(prompt_url)

    resp.record(maxLength='30', action='/finish-recording', finishOnKey='1')

    return str(resp)

@app.route('/finish-recording', methods=['GET', 'POST'])
def finish_recording():
    resp = VoiceResponse()
    recording_url = request.values.get("RecordingUrl", None)
    print recording_url
    resp.say("Thanks! Goodbye.")
    return str(resp)

if __name__ == '__main__':
    app.run(use_reloader=True)
