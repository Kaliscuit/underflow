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
import modules.python_doc.main as python_doc
import modules.douban_movie.main as douban_movie

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
        r.set('xml_p', repr(xml_parser.xml_to_dict(xml_get)))
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

     text_template = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%d</CreateTime>
             <MsgType><![CDATA[%s]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""

    pictextTpl = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%s]]></Url>
                </item>
                </Articles>
                <FuncFlag>1</FuncFlag>
                </xml> """


    if dict['Content'] == u'笑话' or dict['Content'] == 'joke':
        dict['Content'] = joke.get_joke()
        echostr = text_template % (dict['FromUserName'], dict['ToUserName'], int(time.time()), 'text', dict['Content'])
    elif len(dict['Content'].split(' ')) > 1 and dict['Content'].split(' ')[0] == 'python':
        dict['Content'] = python_doc.get_doc(dict['Content'].split(' ')[1])
        echostr = text_template % (dict['FromUserName'], dict['ToUserName'], int(time.time()), 'text', dict['Content'])
    elif len(dict['Content'].split(' ')) > 1 and (dict['Content'].split(' ')[0] == u'电影' or dict['Content'].split(' ')[0] == 'movie'):
        Content = douban_movie.query_movie_info(dict['Content'])
        description = douban_movie.query_movie_details(dict['Content'])
        echostr = pictextTpl % (dict['FromUserName'], dict['ToUserName'], str(int(time.time())),
                                Content["subjects"][0]["title"], description,
                                Content["subjects"][0]["images"]["large"], Content["subjects"][0]["alt"])

    if signature == signature_server:
        return echostr
    else:
        return '0'
        # return repr(signature+timestamp+nonce+echostr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
