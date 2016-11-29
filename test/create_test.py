# coding=utf8

import urllib2
import urllib
import json
import poster as poster
import sys
import oss2
from test_config import LOCALHOST, PORT, DATA_TEXT_PATH

reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime


# 单个创建
def test_create_tender(info):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/create_tender/' % (LOCALHOST, PORT)
    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return json.loads(result)

# 批量创建
def batck_create_tender():
    result = get_province_city_info()
    cityData = json.loads(result)

    f = open(DATA_TEXT_PATH)
    lines = f.readlines()

    tenderData = json.loads(''.join(lines))

    for t in tenderData:
        city = t['city']
        info = {}
        (provinceID, cityID) = get_provinceID_cityID(cityData, city)

        info['provinceID'] = provinceID
        info['cityID'] = cityID
        info['tenderID'] = t['id']
        info['title'] = t['title']
        info['location'] = t['location']
        info['url'] = t['url']
        info['datetime'] = t['date']
        info['detail'] = t['detail']
        response = test_create_tender(info)
        status = response['status']
        if status != 'SUCCESS':
            print 'error ', t['title'], status
            break

# 获取所有的省市信息
def get_province_city_info():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_province_city_info/' % (LOCALHOST, PORT)
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

# 根据城市名称，获取城市ID
def get_provinceID_cityID(info, cityName):
    data = info['data']
    for province in data:
        for city in province['citys']:
            name = city['cityName']
            if cityName in name > 0:
                return (province['provinceID'], city['cityID'])
            else:
                print cityName

# 获取投标列表信息
def get_tender_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_tender_list/' % (LOCALHOST, PORT)
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['searchKey'] = "桥桩"
    info['cityID'] = '63'
    info['provinceID'] = '10'



    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return json.loads(result)

if __name__ == '__main__':
    # get_province_city_info()
    # batck_create_tender()
    get_tender_list()
