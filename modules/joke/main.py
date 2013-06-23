import urllib2
from .. import xml_parser as xml_parser


def strip_tags(html):
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)


def get_joke():
    response = urllib2.urlopen('http://www.djdkx.com/open/randxml')
    html = response.read()
    dict = xml_parser.xml_to_dict(html)
    return strip_tags(dict['content'])