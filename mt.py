import logging

from flask import Flask, request, Response
import requests

app = Flask(__name__)
app.config.from_envvar('MT_CONFIG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: $(message)s'))
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

@app.route('/test')
def test():
    raise RuntimeError('test')

@app.route('/webhook', methods=['GET'])
def get():
    if request.args.get('hub.verify_token') == app.config['TOKEN']:
        return Response(request.args.get('hub.challenge'), mimetype='text/plain')
    return 'wrong token'

@app.route('/webhook', methods=['POST'])
def post():
    for sender, text in extract_text_messages(request.get_json()):
        response = 'You said “%s”' % text
        data = {
            'recipient': {'id': sender},
            'message': {'text': response},
        }
        params = {
            'access_token': app.config['PAGE_ACCESS_TOKEN'],
        }
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages',
            params=params,
            data=data,
        )
        app.logger.debug('graph.facebook.com returned %s', r.status_code)
        app.logger.debug('Response from graph.facebook.com: %r', r.text)
    return 'ok'

def extract_text_messages(data):
    for entry in data['entry']:
        for message in entry['messaging']:
            if message['message'] and message['message']['text']:
                yield message['sender']['id'], message['message']['text']

if __name__ == '__main__':
    app.run(debug=True)
