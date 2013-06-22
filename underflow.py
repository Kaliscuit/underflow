import hashlib
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
token = 'underflow'

@app.route('/')
def hello():
    return 'Hello underflow'


@app.route('/auth', methods=['GET'])
def auth():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    arg_list = [token, timestamp, nonce]
    arg_list = sorted(arg_list)
    arg_str = ''
    for arg in arg_list:
        arg_str += arg
    arg_sha1 = hashlib.sha1()
    arg_sha1.update(arg_str)
    signature_server = arg_sha1.hexdigest()
    if signature == signature_server:
        return echostr
    else:
        return repr(signature+timestamp+nonce+echostr)


if __name__ == '__main__':
    app.debug = True
    app.run()
