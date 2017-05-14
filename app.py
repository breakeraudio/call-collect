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

prompts = ['intro.mp3', 'q2.mp3', 'q3.mp3', 'outro.mp3']


@app.route('/')
def home():
    return 'Hello world'

@app.route('/call-collect', methods=['GET', 'POST'])
def call_collect():
    resp = VoiceResponse()
    prompt = request.values.get('prompt')
    previous_recording = request.values.get('RecordingUrl')
    index = prompts.index(prompt)

    # Save recording from previous prompt
    if previous_recording:
        client = Client(account_sid, auth_token)
        client.messages.create(
            to=to_phone_number,
            from_=from_phone_number,
            body='New reply to prompt %d: %s' % (index + 1, previous_recording))

    # Say the current prompt_url
    prompt_url = app_url(request) + url_for('static', filename='prompts/' + prompt)
    resp.play(prompt_url)

    # Record and go to next prompt, if not the last prompt
    if index < len(prompts) - 1:
        action = '/call-collect?prompt=' + prompts[index + 1]
        resp.record(maxLength='300', action=action, finishOnKey='1')

    return str(resp)

def app_url(req):
    return req.base_url.rsplit('/', 1)[0]

if __name__ == '__main__':
    app.run(use_reloader=True)
