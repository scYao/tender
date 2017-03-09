# coding=utf8

import sys
import urllib
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
YZTOKENID = '2017-03-0915221385c6c4d8009564a1b7a6a44fa38742ff'

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

# 登录
def administrator_login_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/administrator_login_background/' % LOCALHOST
    info = {}
    info['adminName'] = '15951606335'
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

#获取招标公告列表，后台管理
def get_tender_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_list_background/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['cityID'] = '-1'
    info['tokenID'] = YZTOKENID
    info['startDate'] = '-1'
    info['endDate'] = '-1'
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

#获取招标内容
def getTenderDetail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_detail/' % LOCALHOST
    info = {}
    info['tenderID'] = '1b0335ca-7132-4771-8df4-e392a06015d2'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#创建收藏
def createFavorite():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_favorite/' % LOCALHOST
    info = {}
    info['tenderID'] = '1b0335ca-7132-4771-8df4-e392a06015d2'
    info['tag'] = 'tender'
    info['tokenID'] = '2017-03-09093919b788c302127d8e2c04ab50c2721cc5bb'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#取消收藏
def deleteFavorite():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/delete_favorite/' % LOCALHOST
    info = {}
    info['favoriteID'] = '2017-03-09094054db050e2472b9b0f9c37cb63f57e6b398'
    info['tokenID'] = '2017-03-09093919b788c302127d8e2c04ab50c2721cc5bb'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取收藏列表
def getFavoriteList():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_favorite_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-09093919b788c302127d8e2c04ab50c2721cc5bb'
    info['tag'] = 'tender'
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取用户信息
def getUserInfoDetail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_user_info_detail/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-09093919b788c302127d8e2c04ab50c2721cc5bb'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#创建管理员
def create_admin_manager():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_admin_manager/' % LOCALHOST
    info = {}
    info['tel'] = '15951606335'
    info['adminPW'] = '123456'
    info['code'] = '1234'
    info['adminName'] = '一曲广陵散'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def formatDic(info):
    for (key, value) in info.items():
        print '{:<20}'.format(key), '{:^20}'.format('string'), '{:<20}'.format(value)


def common():
    gender = 'male'
    if gender == 'male':
        text = '男'
    else:
        text = '女'

def pythonic():
    gender = 'male'
    text = '男' if gender == 'male' else '女'

if __name__ == '__main__':
    get_tender_list_background()
    # administrator_login_background()
    # create_admin_manager()
    # common()
    # pythonic()
    # register()
    # sendSmsCode()
    # logIn()
    # findPassword()
    # getTenderList()
    # re_generate_search_index()
    # getCityList()
    # getTenderDetail()
    # createFavorite()
    # deleteFavorite()
    # getFavoriteList()
    # getUserInfoDetail()
    # info = {}
    #
    # info['tokenID'] = '2017-03-09093919b788c302127d8e2c04ab50c2721cc5bb'
    # formatDic(info)
