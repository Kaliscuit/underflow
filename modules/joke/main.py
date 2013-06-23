def get_joke():
    response = urllib2.urlopen('http://www.djdkx.com/open/randxml')
    html = response.read()
    dict = parse_xml(html)
    return dict['content']