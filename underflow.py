import hashlib
import redis
from xml.dom import minidom
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
token = 'underflow'
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def parse_xml(xml_str, need_list):
    xmldoc = minidom.parse(xml_str)
    doc_list = []
    for need in need_list:
        doc_list.append(xmldoc.getElementsByTagName(need))
    return doc_list


@app.route('/')
def hello():
    return 'Hello underflow'


@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'POST':
        xml_get = request.data
        r.set('weixin_post', repr(xml_get))
        r.set('xml_p', repr(parse_xml(xml_get, ['ToUserName', 'FromUserName'])))
        
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    # echostr = request.args.get('echostr')
    arg_list = [token, timestamp, nonce]
    arg_list = sorted(arg_list)
    arg_str = ''
    for arg in arg_list:
        arg_str += arg
    arg_sha1 = hashlib.sha1()
    arg_sha1.update(arg_str)
    signature_server = arg_sha1.hexdigest()
    if signature == signature_server:
        return '1'
    else:
        return '0'
        # return repr(signature+timestamp+nonce+echostr)


if __name__ == '__main__':
    app.debug = True
    app.run()
