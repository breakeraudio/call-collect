import os

from flask import Flask, request, redirect, url_for
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Phone number format: +15558675309
to_phone_number = os.environ.get('TO_PHONE_NUMBER')
from_phone_number = os.environ.get('FROM_PHONE_NUMBER')


@app.route('/')
def home():
    return 'Hello world'

@app.route('/incoming-call')
def incoming_call():
    resp = VoiceResponse()
    prompt_url = app_url(request) + url_for('static', filename='prompts/intro.mp3')
    resp.play(prompt_url)

    resp.record(maxLength='30', action='/finish-recording', finishOnKey='1')

    return str(resp)

@app.route('/finish-recording', methods=['GET', 'POST'])
def finish_recording():
    recording_url = request.values.get('RecordingUrl', 'Nope!')
    print recording_url

    client = Client(account_sid, auth_token)
    client.messages.create(
    to=to_phone_number,
    from_=from_phone_number,
    body='Recording is here: ' + recording_url)


    resp = VoiceResponse()
    prompt_url = app_url(request) + url_for('static', filename='prompts/outro.mp3')
    resp.play(prompt_url)
    return str(resp)

def app_url(req):
    return req.base_url.rsplit('/', 1)[0]

if __name__ == '__main__':
    app.run(use_reloader=True)
