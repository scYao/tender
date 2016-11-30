# coding=utf8

import urllib2
import urllib
import json
import poster as poster
import sys
import oss2
from test_config import LOCALHOST, PORT, DATA_TEXT_PATH, ADMIN_TOKEN

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

# 创建一级类型
def create_type1_background(typeName):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/create_type1_background/' % (LOCALHOST, PORT)
    info = {}
    info['tokenID'] = ADMIN_TOKEN
    info['typeName'] = typeName

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

# 创建二级类型
def create_type2_background(type1ID, typeName):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/create_type2_background/' % (LOCALHOST, PORT)
    info = {}
    info['tokenID'] = ADMIN_TOKEN
    info['typeName'] = typeName
    info['superTypeID'] = type1ID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result


# 创建二级类型
def create_type3_background(type2ID, typeName):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/create_type3_background/' % (LOCALHOST, PORT)
    info = {}
    info['tokenID'] = ADMIN_TOKEN
    info['typeName'] = typeName
    info['superTypeID'] = type2ID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

# 创建二级类型
def get_type_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type_list/' % (LOCALHOST, PORT)
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return result

def test_create_all_types():
    jsonInfo = '''[
    {
        "typeName": "房间市政",
        "subTypes": [
            {
                "typeName": "工程类",
                "subTypes": [
                    {
                        "typeName": "施工"
                    },
                    {
                        "typeName": "监理"
                    },
                    {
                        "typeName": "勘察设计"
                    },
                    {
                        "typeName": "基坑支护"
                    },
                    {
                        "typeName": "桩基"
                    }
                ]
            },
            {
                "typeName": "专业类",
                "subTypes": []
            },
            {
                "typeName": "服务类",
                "subTypes": []
            },
            {
                "typeName": "货物类",
                "subTypes": []
            },
            {
                "typeName": "其他",
                "subTypes": []
            }
        ]
    },
    {
        "typeName": "交通航运",
        "subTypes": []
    },
    {
        "typeName": "水利",
        "subTypes": []
    },
    {
        "typeName": "铁路",
        "subTypes": []
    }
]'''
    info = json.loads(jsonInfo)
    for t1 in info:
        t1Name = t1['typeName']
        result = create_type1_background(typeName=t1Name)
        result = json.loads(result)
        status = result['status']
        if status != 'SUCCESS':
            return (False, t1Name)
        type1ID = result['data']
        for t2 in t1['subTypes']:
            t2Name = t2['typeName']
            result2 = create_type2_background(type1ID=type1ID, typeName=t2Name)
            result2 = json.loads(result2)
            status2 = result2['status']
            if status2 != 'SUCCESS':
                return (False, t2Name)
            type2ID = result2['data']
            for t3 in t2['subTypes']:
                t3Name = t3['typeName']
                result3 = create_type3_background(type2ID=type2ID, typeName=t3Name)
                result3 = json.loads(result3)
                status3= result3['status']
                if status3 != 'SUCCESS':
                    return (False, t3Name)
    return (True, None)
if __name__ == '__main__':
    # get_province_city_info()
    # batck_create_tender()
    # get_tender_list()
    # test_create_all_types()
    get_type_list()