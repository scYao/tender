# coding=utf8

import urllib2
import urllib
import json
import poster as poster
import sys
import oss2
from test_config import LOCALHOST, DATA_TEXT_PATH, ADMIN_TOKEN, TYPE1_ID



reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime, timedelta
PORT = 5007
PORT = 5018

# 单个创建
def slash(info):
    t1 = datetime.now()
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/' % (LOCALHOST, PORT)
    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    t2 = datetime.now()
    print 'elapsed:', t2 - t1

    return json.loads(result)

#
def asychander(info):
    t1 = datetime.now()
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_tender_list/' % (LOCALHOST, PORT)
    print upload_url
    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    t2 = datetime.now()
    # print 'elapsed:', t2 - t1

    return json.loads(result)


if __name__ == '__main__':
    param = {}
    param['startIndex'] = 0
    param['pageCount'] = 10
    param['startDate'] = '-1'
    param['endDate'] = '-1'
    param['cityID'] = '-1'

    t1 = datetime.now()
    for x in xrange(100):
        asychander(param)
    t2 = datetime.now()
    print 'elapsed:', t2 - t1