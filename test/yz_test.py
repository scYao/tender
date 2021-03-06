# coding=utf8
#
import sys
import chardet
import urllib
import types
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import jieba
import urllib2
import poster as poster
from test_by_yz_config import ResultManager
from bs4 import BeautifulSoup
import re

# LOCALHOST = '127.0.0.1'
# LOCALHOST = '192.168.30.150'
LOCALHOST = '192.168.30.156'
REMOTE = '121.41.56.218'
YZTOKENID = '2017-03-17145344588f6f132ddf7ccead74dcf06134ad63'

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
def get_tender_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_list/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['cityID'] = '-1'
    info['searchKey'] = '-1'
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取招标公告列表
def wechat_search():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/wechat_search/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['cityID'] = '-1'
    info['searchKey'] = '南京'
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    info['tag'] = 2
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
def get_bidding_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_bidding_list_background/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = YZTOKENID
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    info['cityID'] = '-1'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取招标公告列表
def get_bidding_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_bidding_list/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    info['cityID'] = '-1'
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

#获取公司列表
def get_company_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_list/' % LOCALHOST
    info = {}
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


#找回密码
def find_password():
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

# 搜索，后台
def search():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/search/' % LOCALHOST
    info = {}
    info['tag'] = 2
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['startDate'] = '-1'
    info['endDate'] = '-1'
    info['cityID'] = '63'
    info['tokenID'] = YZTOKENID
    info['searchKey'] = '六合区'
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


# 获取公司图片
def get_company_img_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_img_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['companyID'] = '2017-03-10162147bbd4e62a521b35e887a75b310b6c87b8'
    info['tag'] = 4
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取企业业绩列表，后台
def get_company_achievement_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_achievement_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['companyID'] = '2017-03-1817570920a745ba3dc69398c16b14fd72b09826'
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tag'] = 0
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


# 获取项目经理详情，后台
def get_project_manager_info_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_project_manager_info_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['managerID'] = '2017-03-1818024883175b2ad7e73eb42e980b699e64802a'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取项目经理业绩列表，后台
def get_manager_achievement_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_manager_achievement_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['managerID'] = '2017-03-18180248a90ec6f40486c03d4adbfc3f53086f66'
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tag'] = 0
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取招标数据库列表，后台
def get_company_assistant_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_assistant_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result



# 获取招标数据库列表，后台
def get_grade_1_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_grade_1_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取招标数据库列表，后台
def get_grade_2_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_grade_2_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['gradeID'] = '2017-03-101500404bad30da3e3ad7663281341fdd5ad0ea'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取招标数据库列表，后台
def get_grade_3_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_grade_3_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['gradeID'] = '2017-03-10150041cee6bd9455c5220fe4522990fb794012'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取招标数据库列表，后台
def get_grade_4_list_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_grade_4_list_background/' % LOCALHOST
    info = {}
    info['tokenID'] = YZTOKENID
    info['gradeID'] = '2017-03-10150041ce0944d08ddafa5faa221df5428104eb'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


# 获取招标数据库列表，后台
def create_pushed_tender_by_operator():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_pushed_tender_by_operator/' % LOCALHOST
    info = {}
    info['tokenID'] = '2016-12-171435141c5f22cb8420c728648529041d6b7427'
    info['tenderID'] = '2017-03-231554222453565aec199fdfe7e80c10d51f37f2'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

# 获取经办人推送消息列表
def get_pushed_list_by_operator():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_pushed_list_by_operator/' % LOCALHOST
    info = {}
    info['tokenID'] = '2016-12-171435141c5f22cb8420c728648529041d6b7427'
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

    # 获取经办人推送消息列表


def get_operator_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_operator_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2016-12-171435141c5f22cb8420c728648529041d6b7427'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_tender_doing_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_doing_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2016-12-171435141c5f22cb8420c728648529041d6b7427'
    info['userType'] = 2
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def get_undistributed_tender_list_by_resp():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_undistributed_tender_list_by_resp/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-251443070e1839557d4b287869e57ead5e92edd9'
    info['userType'] = 2
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def get_resp_pushed_list_by_boss():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_resp_pushed_list_by_boss/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-251443070e1839557d4b287869e57ead5e92edd9'
    info['userType'] = 2
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def operate_pushed_tender_info():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/operate_pushed_tender_info/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-251443070e1839557d4b287869e57ead5e92edd9'
    info['state'] = 1
    info['pushedID'] = '2017-03-251319040d9e70af98fff8d9159c49d7c0dbe01d'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_user_info_list_by_boss():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_user_info_list_by_boss/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-290925266599dde9d20f818b7b7c77ddece10adf'
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def create_user_info_by_boss():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_user_info_by_boss/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-03-290925266599dde9d20f818b7b7c77ddece10adf'
    info['tel'] = '12345678910'
    info['userName'] = '测试'
    info['userType'] = 4
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_tender_done_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_done_detail/' % LOCALHOST
    info = {}
    info['tenderID'] = '2017-03-2715392891b4d932fe879d6f28337e0056054488'
    info['tokenID'] = '2017-03-290925266599dde9d20f818b7b7c77ddece10adf'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result



def get_wechat_favorite_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_wechat_favorite_list/' % LOCALHOST
    info = {}
    info['endDate'] = '-1'
    info['startDate'] = '-1'
    info['cityID'] = '-1'
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = ''
    info['tag'] = '1'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_hot_searchkey_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_hot_searchkey_list/' % LOCALHOST
    info = {}
    info['endDate'] = '-1'
    info['startDate'] = '-1'
    info['cityID'] = '-1'
    info['startIndex'] = 0
    info['pageCount'] = 10
    info['tokenID'] = ''
    info['tag'] = '1'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def delete_pushed_tender_by_operator():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/delete_pushed_tender_by_operator/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-04-13153628c6a0f09a06d78462fce33ea791a9effc'
    info['pushedID'] = '2017-04-131536114dc06f390d62bad133d45f82c1eb0d30'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def get_tender_user_info_list_by_boss():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_user_info_list_by_boss/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-04-13155228ba95dd5fd2d8665f3274fbd9dcf538b6'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def create_pushed_tender_by_boss():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/create_pushed_tender_by_boss/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-04-13155228ba95dd5fd2d8665f3274fbd9dcf538b6'
    info['tenderID'] = '2017-04-11163821ac645cd78c34f7fe4b42c30f2a8e91ac'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def get_tender_detail_text():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_tender_detail_text/' % LOCALHOST
    info = {}
    info['tenderID'] = '2017-04-20112040d0e5e6eada4086ca7e0d3712944b8d51'
    info['tokenID'] = ''
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    # print result
    detail = json.loads(result)['data']['detail']
    print detail


def get_bidding_detail_text():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_bidding_detail_text/' % LOCALHOST
    info = {}
    # info['tenderID'] = '2017-04-18145202b84ff4d8d78e8a3a6d5a5dc68cfc4ee3'
    info['tenderID'] = "2017-04-1317091781a8d10c7cfa8168ad19b03d2ae88c8e"
    info['tokenID'] = ''
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    # print result
    print json.loads(result)['data']['detail']


def get_company_certificate_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/get_company_certificate_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-04-13155228ba95dd5fd2d8665f3274fbd9dcf538b6'
    info['companyID'] = '2017-04-20180515136fb45f0afe078fa429b7fe03799461'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#获取公众号人员列表
def wx_get_user_info_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5007/wx_get_user_info_list/' % LOCALHOST
    info = {}
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result










if __name__ == '__main__':
    # def deco(func):
    #     def _deco(a, b):
    #         print("before myfunc() called.")
    #         ret = func(a, b)
    #         print("  after myfunc() called. result: %s" % ret)
    #         return ret
    #     return _deco
    #
    # @deco
    # def myfunc(a, b):
    #     print(" myfunc(%s,%s) called." % (a, b))
    #     return a + b
    #
    # myfunc(1, 2)
    # myfunc(3, 4)
    # postDic = {}
    # postData = {}
    # postData['touser'] = '1111'
    # postData['template_id'] = 'aftmxzzzvvv_EyRClAzu3vDbSn9aztufgsZRq6q1hAs'
    # postData['url'] = 'http://weixin.qq.com/download'
    # postData['data'] = {len(postDic): '----'}
    # postDic = {'11111': postData}
    # postData1 = {}
    # postData1['touser'] = '1111'
    # postData1['template_id'] = 'aftmxzzzvvv_EyRClAzu3vDbSn9aztufgsZRq6q1hAs'
    # postData1['url'] = 'http://weixin.qq.com/download'
    # postData1['data'] = {len(postDic): '======'}
    # postDic['11111']['data'].update(postData1['data'])
    # print postDic
    # title = u'（六合分中心）六合区小北门路（长江路至棠城西路）道路改造工程监理'
    # title = re.sub(r'[\[\]（）]', ' ', title)
    # print title
    # fenciList = jieba.cut_for_search(title)
    #
    # def generate(result):
    #     if result.strip() != '':
    #         print '====', result
    #
    #
    # [generate(result) for result in fenciList]
    # search()
    # wx_get_user_info_list()
    # get_company_certificate_list()
    # get_tender_list()
    # gradeType = u'主项'
    # tag = 0 if gradeType == '主项' else 1
    # print tag
    # search()
    # print '始发布之日止投标企业、企业法定代表人﹑项目经理、委托代理人无行贿犯罪档案查询结果原件。'
    # get_bidding_detail_text()
    # get_tender_detail_text()
    # create_pushed_tender_by_boss()
#     # get_tender_user_info_list_by_boss()
#     # delete_pushed_tender_by_operator()
#     # t1 = datetime.datetime.now()
#     # t2 = None
#     # print t1 > t2
#     # get_hot_searchkey_list()
#     # get_wechat_favorite_list()
#     # wechat_search()
#     # get_tender_done_detail()
#     # create_user_info_by_boss()
#     # get_user_info_list_by_boss()
#     # operate_pushed_tender_info()
#     # get_resp_pushed_list_by_boss()
#     # get_undistributed_tender_list_by_resp()
    get_tender_doing_list()
#     # get_operator_list()
#     # get_pushed_list_by_operator()
#     # create_pushed_tender_by_operator()
#     # create_pushed_tender_by_operator()
#     # find_password()
#     get_grade_1_list_background()
#     # get_grade_2_list_background()
#     # get_grade_3_list_background()
#     # get_grade_4_list_background()
#     # get_company_assistant_list_background()
#     # get_company_achievement_list_background()
#     # get_manager_achievement_list_background()
#     # get_project_manager_info_background()
#     # create_tender()
#     # get_company_img_background()
#     # common()
#     # pythonic()
#
#
#     # get_company_detail_background()
#     # get_company_list_background()
#     # get_company_list()
#
#
#
#
#
#     # get_bid_detail_background()
#     # update_bid_background()
#     # delete_bid_background()
#     # get_tender_detail_background()
#     # delete_tender_background()
#     # update_tender_background()
#     # re_generate_bid_search_index()
#     # search_background()
#     get_bidding_list()
#     # get_bidding_list_background()
#
#     # print datetime.date.today()
#
#
#
#
#
#     # get_user_info_detail_background()
#     # get_user_list_background()
#     # get_tender_list_background()
#     # administrator_login_background()
#     # create_admin_manager()
#
#     # register()
#     # sendSmsCode()
#     # logIn()
#     # findPassword()
#     # getTenderList()
#     # re_generate_search_index()
#     # re_generate_user_search_index()
#     # getCityList()
#     # getTenderDetail()
#     # createFavorite()
#     # deleteFavorite()
#     # getFavoriteList()
#     # # getUserInfoDetail()
#     # info = {}
#     # info['tokenID'] = YZTOKENID
#     # info['companyID'] = '2017-03-1817570920a745ba3dc69398c16b14fd72b09826'
#     # info['startIndex'] = 0
#     # info['pageCount'] = 10
#     # formatDic(info)
#     file_object = '''
# <img class="songs-img" src="http://on2lyilwb.bkt.clouddn.com/xingcai" alt="">
# <img class="songs-img" src="http://on2lyilwb.bkt.clouddn.com/%E8%8D%87%E8%8F%9C.png" alt="">
# <img class="songs-img" src="http://on2lyilwb.bkt.clouddn.com/%E9%9B%8E%E9%B8%A01" alt="">
# <img class="songs-img" src="http://on2lyilwb.bkt.clouddn.com/%E9%9B%8E%E9%B8%A02" alt="">
#
#     '''
#
#     listInfo = file_object.splitlines()
#     if "<img" in listInfo[1]:
#         listInfo = filter(lambda x: x.strip() != '', listInfo)
#         for item in listInfo:
#             startIndex = item.index('http')
#             endIndex = item.index('" alt')
#             print "'" + item[startIndex: endIndex] + "'" + ","
#
#     else:
#         listInfo = filter(lambda x:x.strip() != '', listInfo)
#         # listInfo = filter(lambda x:print x, listInfo)
#         for item in listInfo:
#             print "'" + item.replace('<br>', '').strip() + "'" + ","
#
#
#
#
#
