# coding=utf8
import sys
import types
import xmltodict
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import urllib2
import poster as poster

class ResultManager():
    def __init__(self):
        pass
    def getResult(self, params, upload_url):
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(upload_url, datagen, headers)
        data = urllib2.urlopen(request)
        result = data.read()
        return result