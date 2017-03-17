# coding=utf8

import sys
import urllib
import types
import xmltodict
import datetime
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

#获取招标公告列表，后台管理
def get_bid_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_bid_list_background/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = YZTOKENID
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取公司列表，后台管理
def get_company_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_list_background/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = YZTOKENID
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

# 重新生成中标搜索索引
def re_generate_bid_search_index():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/re_generate_bid_search_index/' % LOCALHOST
    info = {}
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 重新生成搜索索引,用户信息
def re_generate_user_search_index():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/re_generate_user_search_index/' % LOCALHOST
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

#获取招标内容,后台
def get_tender_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['tenderID'] = '1b0335ca-7132-4771-8df4-e392a06015d2'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取中标详情,后台
def get_bid_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_bid_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['biddingID'] = '2017-03-09090748b3690e054504d3adb05fe7bf81753459'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取公司详情,后台
def get_company_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['companyID'] = '2017-03-10145520d255ca48668fd6efa22911543af0df92'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


# 编辑中标,后台
def update_bid_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/update_bid_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['biddingID'] = '2017-03-09090748b3690e054504d3adb05fe7bf81753459'
    info['title'] = '泰山路小学新建工程无锡市泰山路小学新建工程室外市政、体育场地设施以及景观绿化工程'
    info['biddingNum'] = '111'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 删除中标详情,后台
def delete_bid_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/delete_bid_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['biddingID'] = '2017-03-09090748b3690e054504d3adb05fe7bf81753459'
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

# 获取用户信息,后台
def get_user_info_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_user_info_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['userID'] = '2016-12-14124727f7d8e1b0af5314e6f1ef43b773f28a73'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result



#获取用户信息
def get_user_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_user_list_background/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = YZTOKENID
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

# 搜索，后台
def search_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/search_background/' % LOCALHOST
    info = {}
    info['tag'] = 3
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = YZTOKENID
    info['searchKey'] = '无锡'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 编辑招标信息,后台
def update_tender_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/update_tender_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['tenderID'] = '1b0335ca-7132-4771-8df4-e392a06015d2'
    info['title'] = '（南京化学工业园）新庄东村环境整治施工'
    info['location'] = '南京化学工业园'
    info['url'] = ''
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 删除招标信息,后台
def delete_tender_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/delete_tender_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['tenderID'] = '1b0335ca-7132-4771-8df4-e392a06015d2'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 创建tender
def create_tender():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_tender/' % LOCALHOST
    info = {}
    info['title'] = '2016年零星工程无锡高新区C区B74-A地块淤泥整治'
    info['cityID'] = '64'
    info['location'] = ''
    info['url'] = ''
    info['publishDate'] = str(datetime.datetime.now())
    info['detail'] = ''
    info['biddingNum'] = ''
    info['reviewType'] = ''
    info['typeID'] = 1
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result



def formatDic(info):
    for (key, value) in info.items():
        print '{:<20}'.format(key), '{:^20}'.format('string'), '{:<20}'.format(value)





def common():
    data = [
        {'bar', 10}, {'foo', 20}, {'foo', 30}
    ]
    groups = {}
    for (key, value) in data:
        if key in groups:
            groups[key].append(value)
        else:
            groups[key] = [value]
    print groups

from collections import defaultdict
def pythonic():
    data = [
        {'bar', 10}, {'foo', 20}, {'foo', 30}
    ]
    #第一种方法
    groups = {}
    for (key, value) in data:
        groups.setdefault(key, []).append(value)
    print groups
    #第二种方法
    groups = defaultdict(list)
    for (key, value) in data:
        groups[key].append(value)
    print groups


if __name__ == '__main__':
    create_tender()

    # common()
    # pythonic()


    # get_company_detail_background()
    # get_company_list_background()





    # get_bid_detail_background()
    # update_bid_background()
    # delete_bid_background()
    # get_tender_detail_background()
    # delete_tender_background()
    # update_tender_background()
    # re_generate_bid_search_index()
    # search_background()

    # get_bid_list_background()

    # print datetime.date.today()





    # get_user_info_detail_background()
    # get_user_list_background()
    # get_tender_list_background()
    # administrator_login_background()
    # create_admin_manager()

    # register()
    # sendSmsCode()
    # logIn()
    # findPassword()
    # getTenderList()
    # re_generate_search_index()
    # re_generate_user_search_index()
    # getCityList()
    # getTenderDetail()
    # createFavorite()
    # deleteFavorite()
    # getFavoriteList()
    # getUserInfoDetail()
    # info = {}
    # info['tokenID'] = YZTOKENID
    # info['biddingID'] = '2017-03-09090748b3690e054504d3adb05fe7bf81753459'
    # info['title'] = '泰山路小学新建工程无锡市泰山路小学新建工程室外市政、体育场地设施以及景观绿化工程'
    # info['biddingNum'] = '111'
    # formatDic(info)
