# coding=utf8

import urllib2
import urllib
import json
import poster as poster
import sys
import oss2
from test_config import LOCALHOST, PORT, DATA_TEXT_PATH, ADMIN_TOKEN, TYPE1_ID

reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime, timedelta


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
    info['startIndex'] = 1
    info['pageCount'] = 10
    info['searchKey'] = "-1"
    info['cityID'] = '63'
    info['provinceID'] = '10'
    info['period'] = 30
    info['type1ID'] = '-1'
    info['type2ID'] = '-1'
    info['type3ID'] = '-1'



    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return json.loads(result)

# 获取投标id列表
def get_tender_id_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_tender_id_list/' % (LOCALHOST, PORT)
    print upload_url
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return json.loads(result)


# 获取投标详情
def get_tender_detail(tenderID):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_tender_detail/' % (LOCALHOST, PORT)
    info = {}
    info['tenderID'] = tenderID

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

# 获取三级列表树
def get_type_tree_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type_tree_list/' % (LOCALHOST, PORT)
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return result

# 获取一级类型列表
def get_type1_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type1_list/' % (LOCALHOST, PORT)
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

# 获取二级类型列表
def get_type2_list(typeID):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type2_list/' % (LOCALHOST, PORT)
    info = {}
    info['typeID'] = typeID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

# 获取三级类型列表
def get_type3_list(typeID):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type3_list/' % (LOCALHOST, PORT)
    info = {}
    info['typeID'] = typeID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result

def get_type_list():
    result = get_type1_list()
    result = json.loads(result)
    status1 = result['status']
    if status1 != 'SUCCESS':
        return (False, 'get type1 list error')
    type1IDList = result['data']
    for type1 in type1IDList:
        type1ID = type1['typeID']
        result2 = get_type2_list(typeID=type1ID)
        result2 = json.loads(result2)
        status2 = result2['status']
        if status2 != 'SUCCESS':
            return (False, 'error type2 : ' + type1ID)
        type2IDList = result2['data']
        for type2 in type2IDList:
            type2ID = type2['typeID']
            result3 = get_type3_list(typeID=type2ID)
            result3 = json.loads(result3)
            status3 = result3['status']
            if status3 != 'SUCCESS':
                return (False, 'error when get type3 : ' + type2ID)

# 获取省份列表
def get_province_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_province_list/' % (LOCALHOST, PORT)
    info = {}

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result


# 获取城市列表
def get_city_list(provinceID):
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_city_list/' % (LOCALHOST, PORT)
    info = {}
    info['provinceID'] = provinceID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    return result


def test_get_provinces_citys():
    result = get_province_list()
    result = json.loads(result)
    status = result['status']
    if status != 'SUCCESS':
        return (False, 'get province error')

    provinceList = result['data']
    for province in provinceList:
        provinceID = province['provinceID']
        result2 = get_city_list(provinceID=provinceID)
        result2 = json.loads(result2)
        status2 = result2['status']
        if status2 != 'SUCCESS':
            return (False, province['provinceName'])



def test_create_all_types():
    jsonInfo = '''[
    {
        "typeName": "房建市政",
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
                    },
                    {
                        "typeName": "其他"
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
        "typeName": "其他",
        "subTypes": [
            {
                "typeName": "其他",
                "subTypes": [
                    {
                        "typeName": "其他"
                    }
                ]
            }
        ]
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

# 获取二级类型列表
def get_type23_by_type1():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:%s/get_type23_by_type1/' % (LOCALHOST, PORT)
    info = {}
    info['typeID'] =TYPE1_ID

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    data = urllib2.urlopen(request)
    result = data.read()
    print result
    return result

def test_get_tender_list_time():
    dt1 = datetime.now()
    for i in xrange(1, 1000):
        get_tender_list()
        print i
    dt2 = datetime.now()

    print dt2 - dt1

if __name__ == '__main__':
    # get_province_city_info()
    # batck_create_tender()
    get_tender_id_list()
    # d1 = datetime.now()
    # for i in xrange(0, 50):
    #     get_tender_list()
    # d2 = datetime.now()
    # print d2 - d1
    # test_create_all_types()
    # get_type_tree_list()
    # get_type_list()
    # test_get_provinces_citys()
    # get_type23_by_type1()
    # get_tender_detail('005689d8-bfe6-4c7e-9339-072fbded5caa')

    # test_get_tender_list_time()