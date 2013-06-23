# coding=utf-8

import hashlib
import redis
import time
import urllib2
from flask import Flask
from flask import render_template
from flask import request
import modules.xml_parser as xml_parser
import modules.joke.main as joke

app = Flask(__name__)
token = 'underflow'
r = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/')
def hello():
    return 'Hello underflow'


@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'POST':
        xml_get = request.data
        r.set('weixin_post', repr(xml_get))
        r.set('xml_p', repr(parse_xml(xml_get)))
        dict = xml_parser.xml_to_dict(xml_get)
        
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
    if dict['Content'] == u'笑话' or dict['Content'] == 'joke':
        dict['Content'] = joke.get_joke()
    text_template = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%d</CreateTime>
             <MsgType><![CDATA[%s]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""
    text = text_template % (dict['FromUserName'], dict['ToUserName'], int(time.time()), 'text', dict['Content'])
    if signature == signature_server:
        return text
    else:
        return '0'
        # return repr(signature+timestamp+nonce+echostr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
