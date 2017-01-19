import os
from flask import Flask, request
from flask_ask import Ask, statement, question, session
import json
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
ask = Ask(app, "/")


# ALEXA INTENTS
@ask.intent("GeneralIntent")
def general_intent(text):
    response = requests.post(
        'http://speech-analysis-server-ip-address/textfile', data=json.dumps({'text': str(text)}))
    if session.attributes['phase'] == 3:
        return statement('Goodbye, have a nice day')
    statement_text = session.attributes['passage'][session.attributes['phase']]
    session.attributes['phase'] += 1
    return question(statement_text)


@ask.launch
def launch():
    session.attributes['phase'] = 1
    session.attributes['passage'] = [
        '<speak>Welcome to Voice analyzer <break time="1s"/> Please read the first sentence provided to you</speak>',
        '<speak>Very good <break time="2s"/> Now read the second passage </speak>',
        '<speak>Excellent <break time="3s"/> Let us finish this after the third and final passage</speak>'
    ]
    return question(session.attributes['passage'][0])

app.secret_key = 'INSERT YOUR SESSION KEY'
app.config['SESSION_TYPE'] = 'filesystem'


if __name__ == '__main__':
    app.run()
