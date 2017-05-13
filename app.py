import os

from flask import Flask, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# Load environment variables
APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')

@app.route('/')
def home():
    return 'Hello world'

@app.route('/incoming-call')
def incoming_call():
    resp = VoiceResponse()
    prompt_url = APP_URL + url_for('static', filename='prompts/sample.mp3')
    resp.play(prompt_url)
    return str(resp)

if __name__ == '__main__':
    app.run()
