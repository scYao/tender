# coding=utf8
import sys
import types
import xmltodict
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import urllib2
import poster as poster
from test_by_yz_config import ResultManager

LOCALHOST = '127.0.0.1'
REMOTE = '121.41.56.218'

#注册
def register():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/register/' % LOCALHOST
    info = {}
    info['tel'] = '15951606335'
    info['password'] = '123456'
    info['code'] = '1234'
    info['userName'] = '一曲广陵散'
    info['companyName'] = '南京拾旧'
    info['jobPosition'] = 'python-end'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取验证码
def sendSmsCode():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/send_sms_code/' % LOCALHOST
    info = {}
    info['tel'] = '15951606335'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#登录
def logIn():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/login/' % LOCALHOST
    info = {}
    info['tel'] = '15951606335'
    info['password'] = '123456'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取招标公告列表
def getTenderList():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_list/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['cityID'] = '0'
    info['searchKey'] = '化学工业园'
    info['startDate'] = '2016-07-24 00:00:00'
    info['endDate'] = '2016-08-18 00:00:00'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#找回密码
def findPassword():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/find_password/' % LOCALHOST
    info = {}
    info['tel'] = '15951606335'
    info['password'] = '123456'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取城市列表
def getCityList():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_city_list/' % LOCALHOST
    info = {}
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#重新生成搜索索引
def re_generate_search_index():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/re_generate_search_index/' % LOCALHOST
    info = {}
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result



def formatDic(info):
    for (key, value) in info.items():
        print '{:<20}'.format(key), '{:^20}'.format('string'), '{:<20}'.format(value)




if __name__ == '__main__':
    # register()
    # sendSmsCode()
    # logIn()
    # findPassword()
    # getTenderList()
    # re_generate_search_index()
    getCityList()
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['cityID'] = '0'
    info['searchKey'] = '化学工业园'
    info['startDate'] = '2016-07-24 00:00:00'
    info['endDate'] = '2016-08-18 00:00:00'
    formatDic(info)
