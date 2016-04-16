from flask import Flask, request, Response

app = Flask(__name__)
app.config.from_envvar('MT_CONFIG')

@app.route('/webhook')
def webhook():
    if request.args['hub.verify_token'] == app.config['TOKEN']:
        return Response(request.args['hub.challenge'], mimetype='text/plain')
    return Response('wrong token', mimetype='text/plain')
