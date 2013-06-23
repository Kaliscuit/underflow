import urllib2
import ..xml_parser as xml_parser


def get_joke():
    response = urllib2.urlopen('http://www.djdkx.com/open/randxml')
    html = response.read()
    dict = xml_parser.xml_to_dict(html)
    return dict['content']