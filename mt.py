from flask import Flask, request

app = Flask(__name__)
app.config.from_envvar('MT_CONFIG')

@app.route('/webhook')
def webhook():
    if request.form['hub.verify_token'] == app.config['token']:
        return request.form['hub.challenge']
    raise ValueError('Wrong token')
