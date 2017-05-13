from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world'

@app.route('/incoming-call')
def incoming_call():
    resp = VoiceResponse()
    resp.play('http://www.flatterist.com/woiu.mp3')
    return str(resp)

if __name__ == '__main__':
    app.run()
