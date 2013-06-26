# coding=utf-8
import hashlib
import xml.etree.ElementTree as ET
import urllib2
# import requests
import json

def query_movie_info(content):
    """
    这里使用豆瓣的电影search API，通过关键字查询电影信息，这里的关键点是，一是关键字取XML中的Content值，
    二是如果Content中存在汉字，就需要先转码，才能进行请求
    """
    movieurlbase = "http://api.douban.com/v2/movie/search"
    DOUBAN_APIKEY = "04e88153167c8e5a0eb983f94375ab0e"  # 这里需要填写你自己在豆瓣上申请的应用的APIKEY
    searchkeys = urllib2.quote(content.encode("utf-8"))  # 如果Content中存在汉字，就需要先转码，才能进行请求
    url = '%s?q=%s&apikey=%s' % (movieurlbase, searchkeys, DOUBAN_APIKEY)
    # return "<p>{'url': %s}</p>" % url
    # url = '%s%s?apikey=%s' % (movieurlbase, id["Content"], DOUBAN_APIKEY)
    # resp = requests.get(url=url, headers=header)
    resp = urllib2.urlopen(url)
    movie = json.loads(resp.read())
    # return "<p>{'movie': %s}</p>" % movie
    # info = movie["subjects"][0]["title"] + movie["subjects"][0]["alt"]
    # info = movie['title'] + ': ' + ''.join(movie['summary'])
    return movie
    # return info
 
def query_movie_details(content):
    """
    这里使用豆瓣的电影subject API，通过在query_movie_info()中拿到的电影ID，来获取电影的summary。
    """
    movieurlbase = "http://api.douban.com/v2/movie/subject/"
    DOUBAN_APIKEY = "04e88153167c8e5a0eb983f94375ab0e"  # 这里需要填写你自己在豆瓣上申请的应用的APIKEY
    id = query_movie_info(content)
    url = '%s%s?apikey=%s' % (movieurlbase, id["subjects"][0]["id"], DOUBAN_APIKEY)
    resp = urllib2.urlopen(url)
    description = json.loads(resp.read())
    description = ''.join(description['summary'])
    return description