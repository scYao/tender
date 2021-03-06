# coding=utf8
import sys

from flask import request

sys.path.append('..')
import json
from models.flask_app import app
from user.AdminManager import AdminManager
from tender.TenderManager import TenderManager
from type.Type1Manager import Type1Manager
from type.Type2Manager import Type2Manager
from type.Type3Manager import Type3Manager
from province.ProvinceManager import ProvinceManager
from user.UserManager import UserManager
from favorite.FavoriteManager import FavoriteManager
from company.CompanyManager import CompanyManager
from company.CompanyAchievementManager import CompanyAchievementManager
from company.DelinquenentConductManager import DelinquenentConductManager
from company.CompanyCertificateManager import CompanyCertificateManager
from projectManager.PMManager import PMManager
from projectManager.LicenseManager import LicenseManager
from projectManager.PMAchievementManager import PMAchievementManager
from certificationGrade.CertificationGrade1Manager import CertificationGrade1Manager
from certificationGrade.CertificationGrade2Manager import CertificationGrade2Manager
from certificationGrade.CertificationGrade3Manager import CertificationGrade3Manager
from certificationGrade.CertificationGrade4Manager import CertificationGrade4Manager
from winBidding.WinBiddingManager import WinBiddingManager
from winBidding.CandidateManager import CandidateManager
from search.SearchManager import SearchManager
from image.ImageManager import ImageManager
from company.CompanyAssistantManager import CompanyAssistantManager
from message.MessageManager import MessageManager
from user.OperatorManager import OperatorManager
from user.ResponsiblePersonManager import ResponsiblePersonManager
from user.AuditorManager import AuditorManager
from user.BossManager import BossManager
from pushedTender.PushedTenderManager import PushedTenderManager
from news.NewsManager import NewsManager
from user.UserBaseManager import UserBaseManager
from tender.SubscribedKeyManager import SubscribedKeyManager
from wechatPublic.WechatManager import WechatManager
from wechatPublic.WechatMessageManager import WechatMessageManager
from stoken.StsTokenManager import StsTokenManager
from fileInfo.FileInfoManager import FileInfoManager
from department.DepartmentAreaManager import DepartmentAreaManager
from contract.ContractManager import ContractManager
from contract.ContractProjectProcessManager import ContractProjectProcessManager
from contract.ContractFinalAccountsManager import ContractFinalAccountsManager
from contract.ContractEmergencyManager import ContractEmergencyManager

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 管理员登录，后台管理
@app.route('/administrator_login_background/', methods=['POST', 'GET'])
def administrator_login_background():
    if request.method == 'POST':
        paramsJson = request.form['data']
        adminManager = AdminManager()
        (status, ret) = adminManager.adminLogin(paramsJson)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)

# 创建投标信息
@app.route('/create_tender/', methods=['POST', 'GET'])
def create_tender():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.createTender(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 判断招标信息是否存在
@app.route('/does_tender_exists/', methods=['POST', 'GET'])
def does_tender_exists():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.doesTenderExists(info=json.loads(paramsJson))
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 创建投标信息，后台
@app.route('/create_tender_background/', methods=['POST', 'GET'])
def create_tender_background():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.createTender(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 编辑招标信息，后台
@app.route('/update_tender_background/', methods=['POST', 'GET'])
def update_tender_background():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.updateTenderBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 删除招标信息，后台
@app.route('/delete_tender_background/', methods=['POST', 'GET'])
def delete_tender_background():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.deleteTenderBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取投标信息列表
@app.route('/get_tender_list/', methods=['POST', 'GET'])
def get_tender_list():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取招标列表, 标志是否被push
@app.route('/get_tender_list_with_pushed_tag/', methods=['POST', 'GET'])
def get_tender_list_with_pushed_tag():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderListWithPushedTag(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)


# 获取投标信息列表,后台使用
@app.route('/get_tender_list_background/', methods=['POST', 'GET'])
def get_tender_list_background():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)


# 获取中标信息列表,后台使用
@app.route('/get_bidding_list_background/', methods=['POST', 'GET'])
def get_bidding_list_background():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息列表
@app.route('/get_bidding_list/', methods=['POST', 'GET'])
def get_bidding_list():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息列表
@app.route('/get_bidding_list_by_company_id_background/', methods=['POST', 'GET'])
def get_bidding_list_by_company_id_background():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingListByCompanyIDBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取公司列表,后台使用
@app.route('/get_company_list_background/', methods=['POST', 'GET'])
def get_company_list_background():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取公司列表
@app.route('/get_company_list/', methods=['POST', 'GET'])
def get_company_list():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取投标信息详情
@app.route('/get_tender_detail/', methods=['POST', 'GET'])
def get_tender_detail():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取投标信息详情
@app.route('/get_tender_detail_text/', methods=['POST', 'GET'])
def get_tender_detail_text():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderDetailText(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取投标信息详情
@app.route('/get_tender_detail_for_wechat_app/', methods=['POST', 'GET'])
def get_tender_detail_for_wechat_app():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderDetailForWechatApp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取投标信息详情,后台
@app.route('/get_tender_detail_background/', methods=['POST', 'GET'])
def get_tender_detail_background():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.getTenderDetailBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息详情,后台
@app.route('/get_bidding_detail_background/', methods=['POST', 'GET'])
def get_bidding_detail_background():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingDetailBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息详情
@app.route('/get_bidding_detail/', methods=['POST', 'GET'])
def get_bidding_detail():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息详情
@app.route('/get_bidding_detail_text/', methods=['POST', 'GET'])
def get_bidding_detail_text():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBiddingDetailText(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取中标信息详情
@app.route('/get_bid_detail/', methods=['POST', 'GET'])
def get_bid_detail():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBidDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取企业详情,后台
@app.route('/get_company_detail_background/', methods=['POST', 'GET'])
def get_company_detail_background():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyDetailBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取企业详情
@app.route('/get_company_detail/', methods=['POST', 'GET'])
def get_company_detail():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取索引tenderID
@app.route('/get_tender_id_list/', methods=['POST', 'GET'])
def get_tender_id_list():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        (status, jsonlist) = tenderManager.getTenderIDList()
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取全部省市信息
@app.route('/get_province_city_info/', methods=['POST', 'GET'])
def get_province_city_info():
    tenderManager = TenderManager()

    data = {}
    data['status'] = 'SUCCESS'
    (status, result) = tenderManager.getProvinceCityInfo()
    data['data'] = result
    return json.dumps(data)

# 后台管理, 创建一级类型
@app.route('/create_type1_background/', methods=['POST', 'GET'])
def create_type1_background():
    type1Manager = Type1Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type1Manager.createType1Background(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 后台管理, 创建二级类型
@app.route('/create_type2_background/', methods=['POST', 'GET'])
def create_type2_background():
    type2Manager = Type2Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type2Manager.createType2Background(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 后台管理, 创建三级类型
@app.route('/create_type3_background/', methods=['POST', 'GET'])
def create_type3_background():
    type3Manager = Type3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type3Manager.createType3Background(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取索引类型树
@app.route('/get_type_list/', methods=['POST', 'GET'])
def get_type_list():
    type3Manager = Type3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':

        (status, jsonlist) = type3Manager.getTypeList()
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取一级类型
@app.route('/get_type1_list/', methods=['POST', 'GET'])
def get_type1_list():
    type1Manager = Type1Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        (status, jsonlist) = type1Manager.getType1List()
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取二级类型
@app.route('/get_type2_list/', methods=['POST', 'GET'])
def get_type2_list():
    type2Manager = Type2Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type2Manager.getType2List(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取三级类型
@app.route('/get_type3_list/', methods=['POST', 'GET'])
def get_type3_list():
    type3Manager = Type3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type3Manager.getType3List(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 通过类型1ID获取类型2和3的树
@app.route('/get_type23_by_type1/', methods=['POST', 'GET'])
def get_type23_by_type1():
    type3Manager = Type3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = type3Manager.getType23ByType1(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取省列表
@app.route('/get_province_list/', methods=['POST', 'GET'])
def get_province_list():
    provinceManager = ProvinceManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        (status, jsonlist) = provinceManager.getProvinceList()
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取城市列表
@app.route('/get_city_list/', methods=['POST', 'GET'])
def get_city_list():
    provinceManager = ProvinceManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = provinceManager.getCityList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 发送短信验证码
@app.route('/send_sms_code/', methods=['POST', 'GET'])
def send_sms_code():
    if request.method == 'POST':
        paramsJson = request.form['data']
        userManager = UserManager()
        (status, ret) = userManager.sendSMS(paramsJson)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)


# 新的登录函数
@app.route('/login/', methods=['POST', 'GET'])
def login():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.login(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# oa系统登录函数
@app.route('/oa_login/', methods=['POST', 'GET'])
def oa_login():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.oaLogin(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 微信小程序使用微信登录
@app.route('/login_with_wechat/', methods=['POST', 'GET'])
def login_with_wechat():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.loginWithWechat(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取用户详情
@app.route('/get_user_info_detail/', methods=['POST', 'GET'])
def get_user_info_detail():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.getUserInfoDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取用户详情,后台
@app.route('/get_user_info_detail_background/', methods=['POST', 'GET'])
def get_user_info_detail_background():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.getUserInfoDetailBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 更新用户信息
@app.route('/update_user_info/', methods=['POST', 'GET'])
def update_user_info():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.updateUserInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 找回密码
@app.route('/find_password/', methods=['POST', 'GET'])
def find_password():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.findPasswordWithSmsCode(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 注册, 有短信验证码校验
@app.route('/register/', methods=['POST', 'GET'])
def register():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        params = request.form['data']
        info = json.loads(params)
        # info['ipAddress'] = request.headers['X-Forwarded-For']
        info['ipAddress'] = '127.0.0.1'
        jsonInfo = json.dumps(info)
        (status, userID) = userManager.register(jsonInfo)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = userID

    return json.dumps(data)

#创建管理者
@app.route('/create_admin_manager/', methods=['POST', 'GET'])
def create_admin_manager():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        params = request.form['data']
        info = json.loads(params)
        # info['ipAddress'] = request.headers['X-Forwarded-For']
        info['ipAddress'] = '127.0.0.1'
        jsonInfo = json.dumps(info)
        (status, userID) = userManager.createAdminManager(jsonInfo)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = userID
    return json.dumps(data)

#小程序使用，获取我的关注列表
@app.route('/get_wechat_favorite_list/', methods=['POST', 'GET'])
def get_wechat_favorite_list():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.getWechatFavoriteList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取收藏列表, 招标
@app.route('/get_favorite_tender_list/', methods=['POST', 'GET'])
def get_favorite_tender_list():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.getFavoriteTenderList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取收藏列表, 中标
@app.route('/get_favorite_win_bidding_list/', methods=['POST', 'GET'])
def get_favorite_win_bidding_list():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.getFavoriteWinBiddingList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建收藏
@app.route('/create_favorite/', methods=['POST', 'GET'])
def create_favorite():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.createFavorite(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 取消收藏
@app.route('/delete_favorite/', methods=['POST', 'GET'])
def delete_favorite():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.deleteFavorite(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 创建公司
@app.route('/create_company/', methods=['POST', 'GET'])
def create_company():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyManager.createCompany(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建公司, 上传图片
@app.route('/upload_company_image/', methods=['POST', 'GET'])
def upload_company_image():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyManager.uploadCompanyImage(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建项目经理表
@app.route('/create_project_manager/', methods=['POST', 'GET'])
def create_project_manager():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.createProjectManager(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取项目经理列表,  后台管理
@app.route('/get_project_manager_list_background/', methods=['POST', 'GET'])
def get_project_manager_list_background():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getProjectManagerListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取项目经理列表
@app.route('/get_project_manager_list/', methods=['POST', 'GET'])
def get_project_manager_list():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getProjectManagerListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 创建项目经理证件表
@app.route('/create_manager_license/', methods=['POST', 'GET'])
def create_manager_license():
    licenseManager = LicenseManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = licenseManager.createManagerLicense(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建项目经理业绩表
@app.route('/create_manager_achievement/', methods=['POST', 'GET'])
def create_manager_achievement():
    achievementManager = PMAchievementManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = achievementManager.createManagerAchievement(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取项目经理业绩列表
@app.route('/get_pm_achievement_list/', methods=['POST', 'GET'])
def get_pm_achievement_list():
    achievementManager = PMAchievementManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = achievementManager.getPMAchievementList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建公司业绩表
@app.route('/create_company_achievement/', methods=['POST', 'GET'])
def create_company_achievement():
    companyAchievementManager = CompanyAchievementManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyAchievementManager.createCompanyAchievement(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建公司资质表
@app.route('/create_company_certificate/', methods=['POST', 'GET'])
def create_company_certificate():
    companyCertificateManager = CompanyCertificateManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyCertificateManager.createCompanyCertificate(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建公司不良信息表
@app.route('/create_delinquenent_conduct/', methods=['POST', 'GET'])
def create_delinquenent_conduct():
    delinquenentConductManager = DelinquenentConductManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = delinquenentConductManager.createDelinquenentConduct(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取公司不良信息列表, 后台管理
@app.route('/get_delinquenent_conduct_list_background/', methods=['POST', 'GET'])
def get_delinquenent_conduct_list_background():
    delinquenentConductManager = DelinquenentConductManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = delinquenentConductManager.getDelinquenentConductListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取公司不良信息列表
@app.route('/get_delinquenent_conduct_list/', methods=['POST', 'GET'])
def get_delinquenent_conduct_list():
    delinquenentConductManager = DelinquenentConductManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = delinquenentConductManager.getDelinquenentConductListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建一级资质等级
@app.route('/create_certification_grade1/', methods=['POST', 'GET'])
def create_certification_grade1():
    certificationGrade1Manager = CertificationGrade1Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade1Manager.createCertificationGrade1(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)



# 创建二级资质等级
@app.route('/create_certification_grade2/', methods=['POST', 'GET'])
def create_certification_grade2():
    certificationGrade2Manager = CertificationGrade2Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade2Manager.createCertificationGrade2(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建三级资质等级
@app.route('/create_certification_grade3/', methods=['POST', 'GET'])
def create_certification_grade3():
    certificationGrade3Manager = CertificationGrade3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade3Manager.createCertificationGrade3(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建四级资质等级
@app.route('/create_certification_grade4/', methods=['POST', 'GET'])
def create_certification_grade4():
    certificationGrade4Manager = CertificationGrade4Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade4Manager.createCertificationGrade4(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建中标公示
@app.route('/create_win_bidding/', methods=['POST', 'GET'])
def create_win_bidding():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = winBiddingManager.createWinBidding(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建中标候选人
@app.route('/create_candidate/', methods=['POST', 'GET'])
def create_candidate():
    candidateManager = CandidateManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = candidateManager.createCandidate(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#重新生成搜索索引
@app.route('/re_generate_search_index/', methods=['POST', 'GET'])
def re_generate_search_index():
    tenderManager = TenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = tenderManager.reGenerateSearchIndex(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 重新生成搜索索引，中标
@app.route('/re_generate_bidding_search_index/', methods=['POST', 'GET'])
def re_generate_bidding_search_index():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.reGenerateBiddingSearchIndex(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 重新生成搜索索引
@app.route('/re_generate_user_search_index/', methods=['POST', 'GET'])
def re_generate_user_search_index():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = userManager.reGenerateUserSearchIndex(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)


# 获取用户信息列表，后台
@app.route('/get_user_list_background/', methods=['POST', 'GET'])
def get_user_list_background():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userManager.getUserListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 搜索，后台
@app.route('/search_background/', methods=['POST', 'GET'])
def search_background():
    searchManager = SearchManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = searchManager.searchBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 搜索
@app.route('/search/', methods=['POST', 'GET'])
def search():
    searchManager = SearchManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = searchManager.searchBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#获取热门搜索关键词，小程序使用
@app.route('/get_hot_searchkey_list/', methods=['POST', 'GET'])
def get_hot_searchkey_list():
    searchManager = SearchManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = searchManager.getHotSearchkeyList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#微信小程序，搜索
@app.route('/wechat_search/', methods=['POST', 'GET'])
def wechat_search():
    searchManager = SearchManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = searchManager.wechatSearch(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 编辑中标信息，后台
@app.route('/update_bidding_background/', methods=['POST', 'GET'])
def update_bidding_background():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.updateBiddingBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 删除中标信息，后台
@app.route('/delete_bidding_background/', methods=['POST', 'GET'])
def delete_bidding_background():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.deleteBiddingBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取公司图片，后台
@app.route('/get_company_img_background/', methods=['POST', 'GET'])
def get_company_img_background():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyImgBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取公司图片，后台
@app.route('/get_company_img/', methods=['POST', 'GET'])
def get_company_img():
    companyManager = CompanyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyManager.getCompanyImg(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 删除中标信息，后台
@app.route('/does_image_exists/', methods=['POST', 'GET'])
def does_image_exists():
    imageManager = ImageManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = imageManager.doesImageExists(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)


# 获取企业业绩列表，后台
@app.route('/get_company_achievement_list_background/', methods=['POST', 'GET'])
def get_company_achievement_list_background():
    companyAchievementManager = CompanyAchievementManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyAchievementManager.getCompanyAchievementListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

# 获取企业业绩列表
@app.route('/get_company_achievement_list/', methods=['POST', 'GET'])
def get_company_achievement_list():
    companyAchievementManager = CompanyAchievementManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = companyAchievementManager.getCompanyAchievementList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)


# 获取项目经理详情，后台
@app.route('/get_project_manager_info_background/', methods=['POST', 'GET'])
def get_project_manager_info_background():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getProjectManagerInfoBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取项目经理详情
@app.route('/get_project_manager_info/', methods=['POST', 'GET'])
def get_project_manager_info():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getProjectManagerInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取项目经理业绩列表，后台
@app.route('/get_manager_achievement_list_background/', methods=['POST', 'GET'])
def get_manager_achievement_list_background():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getManagerAchievementListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取项目经理业绩列表
@app.route('/get_manager_achievement_list/', methods=['POST', 'GET'])
def get_manager_achievement_list():
    pMManager = PMManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pMManager.getManagerAchievementList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建CompanyAssistant
@app.route('/get_company_assistant_list_background/', methods=['POST', 'GET'])
def get_company_assistant_list_background():
    companyAssistatntManager = CompanyAssistantManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyAssistatntManager.getCompanyAssistantListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取一级资质等级列表
@app.route('/get_grade_1_list_background/', methods=['POST', 'GET'])
def get_grade_1_list_background():
    certificationGrade1Manager = CertificationGrade1Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade1Manager.getGrade1ListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取2级资质等级列表
@app.route('/get_grade_2_list_background/', methods=['POST', 'GET'])
def get_grade_2_list_background():
    certificationGrade2Manager = CertificationGrade2Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade2Manager.getGrade2ListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取3级资质等级列表
@app.route('/get_grade_3_list_background/', methods=['POST', 'GET'])
def get_grade_3_list_background():
    certificationGrade3Manager = CertificationGrade3Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade3Manager.getGrade3ListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取4级资质等级列表
@app.route('/get_grade_4_list_background/', methods=['POST', 'GET'])
def get_grade_4_list_background():
    certificationGrade4Manager = CertificationGrade4Manager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = certificationGrade4Manager.getGrade4ListBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取未读消息列表
@app.route('/get_message_list/', methods=['POST', 'GET'])
def get_message_list():
    messageManager = MessageManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = messageManager.getMessageList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除未读消息
@app.route('/delete_messages/', methods=['POST', 'GET'])
def delete_messages():
    messageManager = MessageManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = messageManager.deleteMessages(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 创建经办人, 分配工作给经办人
@app.route('/create_operator/', methods=['POST', 'GET'])
def create_operator():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.createOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人获取 正在进行中的招标详情
@app.route('/get_doing_detail_by_resp/', methods=['POST', 'GET'])
def get_doing_detail_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getDoingDetailByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人, 批注进行中的项目
@app.route('/create_tender_comment_by_resp/', methods=['POST', 'GET'])
def create_tender_comment_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.createTenderCommentByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人, 删除批注
@app.route('/delete_tender_comment_by_resp/', methods=['POST', 'GET'])
def delete_tender_comment_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.deleteTenderCommentByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人获取待分配列表
@app.route('/get_undistributed_tender_list_by_resp/', methods=['POST', 'GET'])
def get_undistributed_tender_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getUndistributedTenderListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人填写进行中项目的报价信息
@app.route('/create_quoted_price_by_resp/', methods=['POST', 'GET'])
def create_quoted_price_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.createQuotedPriceByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人获取待分配列表
@app.route('/get_distributed_tender_list_by_resp/', methods=['POST', 'GET'])
def get_distributed_tender_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getDistributedTenderListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 重新分配经办人
@app.route('/update_operator/', methods=['POST', 'GET'])
def update_operator():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.updateOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人获取我的推送列表
@app.route('/get_pushed_list_by_resp/', methods=['POST', 'GET'])
def get_pushed_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getPushedListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人从经办人推送列表推送
@app.route('/update_pushed_tender_by_resp/', methods=['POST', 'GET'])
def update_pushed_tender_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.updatePushedTenderByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人 获取某个经办人的推送列表
@app.route('/get_operator_pushed_list_by_resp/', methods=['POST', 'GET'])
def get_operator_pushed_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getOperatorPushedListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人 获取所有推送列表
@app.route('/get_all_pushed_list_by_resp/', methods=['POST', 'GET'])
def get_all_pushed_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getAllPushedListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建推送
@app.route('/create_pushed_tender_by_operator/', methods=['POST', 'GET'])
def create_pushed_tender_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.createPushedTenderByOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 取消推送，经办人
@app.route('/delete_pushed_tender_by_operator/', methods=['POST', 'GET'])
def delete_pushed_tender_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.deletePushedTenderByOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 创建推送, 自定义标
@app.route('/create_customized_tender_by_operator/', methods=['POST', 'GET'])
def create_customized_tender_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        (status, result) = operatorManager.createCustomizedTenderByOperator(jsonInfo=paramsJson, imgFileList=imgList)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 添加项目信息
@app.route('/update_doing_pushed_tender/', methods=['POST', 'GET'])
def update_doing_pushed_tender():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.updateDoingPushedTender(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        print json.dumps(result)
        return json.dumps(data)

# 已经完成，添加项目信息
@app.route('/update_done_pushed_tender/', methods=['POST', 'GET'])
def update_done_pushed_tender():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.updateDonePushedTender(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 已经完成的项目信息详情
@app.route('/get_tender_done_detail/', methods=['POST', 'GET'])
def get_tender_done_detail():
    pushedTenderManager = PushedTenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pushedTenderManager.getTenderDoneDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取自定义项目的详情
@app.route('/get_customized_tender_detail/', methods=['POST', 'GET'])
def get_customized_tender_detail():
    pushedTenderManager = PushedTenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pushedTenderManager.getCustomizedTenderDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 正在进行中的列表
@app.route('/get_tender_doing_list/', methods=['POST', 'GET'])
def get_tender_doing_list():
    pushedTenderManager = PushedTenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pushedTenderManager.getTenderDoingList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取经办人列表
@app.route('/get_operator_list/', methods=['POST', 'GET'])
def get_operator_list():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.getUserList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建打保证金等记录
@app.route('/create_operation/', methods=['POST', 'GET'])
def create_operation():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.createOperation(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 上传标书
@app.route('/create_operation_bidding_book_by_operator/', methods=['POST', 'GET'])
def create_operation_bidding_book_by_operator():
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        operatorManager = OperatorManager()
        (status, ret) = operatorManager.createOperationBiddingBookByOperator(paramsJson, imgList)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)

# 获取经办人的推送
@app.route('/get_pushed_list_by_operator/', methods=['POST', 'GET'])
def get_pushed_list_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.getPushedListByOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取经办人的推送列表,其他途经
@app.route('/get_customized_pushed_list_by_operator/', methods=['POST', 'GET'])
def get_customized_pushed_list_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.getCustomizedPushedListByOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 已完成的列表
@app.route('/get_tender_done_list/', methods=['POST', 'GET'])
def get_tender_done_list():
    pushedTenderManager = PushedTenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pushedTenderManager.getTenderDoneList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 历史记录列表
@app.route('/get_tender_history_list/', methods=['POST', 'GET'])
def get_tender_history_list():
    pushedTenderManager = PushedTenderManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = pushedTenderManager.getTenderHistoryList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人获取我的推送列表
@app.route('/get_pushed_list_by_auditor/', methods=['POST', 'GET'])
def get_pushed_list_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getPushedListByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人获取 正在进行中的招标详情
@app.route('/get_doing_detail_by_auditor/', methods=['POST', 'GET'])
def get_doing_detail_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getDoingDetailByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人填写进行中项目的报价信息
@app.route('/create_quoted_price_by_auditor/', methods=['POST', 'GET'])
def create_quoted_price_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.createQuotedPriceByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 获取负责人推送列表
@app.route('/get_resp_pushed_list_by_auditor/', methods=['POST', 'GET'])
def get_resp_pushed_list_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getRespPushedListByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 获取某个经办人的推送列表
@app.route('/get_operator_pushed_list_by_auditor/', methods=['POST', 'GET'])
def get_operator_pushed_list_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getOperatorPushedListByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 获取所以推送列表
@app.route('/get_all_pushed_list_by_auditor/', methods=['POST', 'GET'])
def get_all_pushed_list_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getAllPushedListByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人获取我的推送数据分析
@app.route('/get_data_info_by_auditor/', methods=['POST', 'GET'])
def get_data_info_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getDataInfoByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#负责人创建推送
@app.route('/create_pushed_tender_by_resp/', methods=['POST', 'GET'])
def create_pushed_tender_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.createPushedTenderByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人取消推送
@app.route('/delete_pushed_tender_by_resp/', methods=['POST', 'GET'])
def delete_pushed_tender_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.deletePushedTenderByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人获取我的推送数据分析
@app.route('/get_data_info_by_resp/', methods=['POST', 'GET'])
def get_data_info_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getDataInfoByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 创建推送, 自定义标, 负责人
@app.route('/create_customized_tender_by_resp/', methods=['POST', 'GET'])
def create_customized_tender_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        (status, result) = responsiblePersonManager.createCustomizedTenderByResp(jsonInfo=paramsJson, imgFileList=imgList)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#负责人获取推送人员列表
@app.route('/get_tender_user_info_list_by_resp/', methods=['POST', 'GET'])
def get_tender_user_info_list_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getTenderUserInfoListByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取所有员工的推送信息 负责人
@app.route('/get_all_data_info_by_resp/', methods=['POST', 'GET'])
def get_all_data_info_by_resp():
    responsiblePersonManager = ResponsiblePersonManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = responsiblePersonManager.getAllDataInfoByResp(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 负责人上传标书
@app.route('/create_operation_bidding_book_by_resp/', methods=['POST', 'GET'])
def create_operation_bidding_book_by_resp():
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        responsiblePersonManager = ResponsiblePersonManager()
        (status, ret) = responsiblePersonManager.createOperationBiddingBookByResp(paramsJson, imgList)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)

#审核人创建推送
@app.route('/create_pushed_tender_by_auditor/', methods=['POST', 'GET'])
def create_pushed_tender_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.createPushedTenderByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人撤销推送
@app.route('/delete_pushed_tender_by_auditor/', methods=['POST', 'GET'])
def delete_pushed_tender_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.deletePushedTenderByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人创建自定义标段并推送
@app.route('/create_customized_tender_by_auditor/', methods=['POST', 'GET'])
def create_customized_tender_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        (status, result) = auditorManager.createCustomizedTenderByAuditor(jsonInfo=paramsJson, imgFileList=imgList)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人上传标书
@app.route('/create_operation_bidding_book_by_auditor/', methods=['POST', 'GET'])
def create_operation_bidding_book_by_auditor():
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        auditorManager = AuditorManager()
        (status, ret) = auditorManager.createOperationBiddingBookByAuditor(paramsJson, imgList)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)

#审定人创建推送
@app.route('/create_pushed_tender_by_boss/', methods=['POST', 'GET'])
def create_pushed_tender_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createPushedTenderByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 审定人暂停用户
@app.route('/disable_user_by_boss/', methods=['POST', 'GET'])
def disable_user_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.disableUserByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人激活用户
@app.route('/enable_user_by_boss/', methods=['POST', 'GET'])
def enable_user_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.enableUserByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人撤销推送
@app.route('/delete_pushed_tender_by_boss/', methods=['POST', 'GET'])
def delete_pushed_tender_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deletePushedTenderByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人创建推送, 自定义标段
@app.route('/create_customized_tender_by_boss/', methods=['POST', 'GET'])
def create_customized_tender_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'

    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        (status, result) = bossManager.createCustomizedTenderByBoss(jsonInfo=paramsJson, imgFileList=imgList)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人批注正在进行中的项目
@app.route('/create_tender_comment_by_boss/', methods=['POST', 'GET'])
def create_tender_comment_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createTenderCommentByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人删除批注
@app.route('/delete_tender_comment_by_boss/', methods=['POST', 'GET'])
def delete_tender_comment_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deleteTenderCommentByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人填写进行中项目的报价信息
@app.route('/create_quoted_price_by_boss/', methods=['POST', 'GET'])
def create_quoted_price_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createQuotedPriceByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人获取待分配列表
@app.route('/get_undistributed_tender_list_by_boss/', methods=['POST', 'GET'])
def get_undistributed_tender_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getUndistributedTenderListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人获取已分配列表
@app.route('/get_distributed_tender_list_by_boss/', methods=['POST', 'GET'])
def get_distributed_tender_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDistributedTenderListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 审定人 获取负责人推送列表
@app.route('/get_resp_pushed_list_by_boss/', methods=['POST', 'GET'])
def get_resp_pushed_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getRespPushedListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 获取某个经办人的推送列表
@app.route('/get_operator_pushed_list_by_boss/', methods=['POST', 'GET'])
def get_operator_pushed_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getOperatorPushedListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 回收站列表
@app.route('/get_discard_pushed_list_by_boss/', methods=['POST', 'GET'])
def get_discard_pushed_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDiscardPushedListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 从回收站回收
@app.route('/recover_pushed_tender_by_boss/', methods=['POST', 'GET'])
def recover_pushed_tender_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.recoverPushedTenderByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 获取所以推送列表
@app.route('/get_all_pushed_list_by_boss/', methods=['POST', 'GET'])
def get_all_pushed_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getAllPushedListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 审定人获取 审核人的推送列表
@app.route('/get_auditor_pushed_list_by_boss/', methods=['POST', 'GET'])
def get_auditor_pushed_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getAuditorPushedListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 决定是否要投标
@app.route('/operate_pushed_tender_info/', methods=['POST', 'GET'])
def operate_pushed_tender_info():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.operatePushedTenderInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 决定是否要投标
@app.route('/get_all_data_info_by_boss/', methods=['POST', 'GET'])
def get_all_data_info_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getAllDataInfoByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 获取部门列表
@app.route('/get_department_list_by_boss/', methods=['POST', 'GET'])
def get_department_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDepartmentListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 创建部门
@app.route('/create_department_by_boss/', methods=['POST', 'GET'])
def create_department_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createDepartmentByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 删除部门
@app.route('/delete_department_by_boss/', methods=['POST', 'GET'])
def delete_department_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deleteDepartmentByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 更新部门
@app.route('/update_department_by_boss/', methods=['POST', 'GET'])
def update_department_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.updateDepartmentByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 更新部门
@app.route('/get_department_by_id/', methods=['POST', 'GET'])
def get_department_by_id():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDepartmentByID(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 获取部门区域列表
@app.route('/get_department_area_list_by_boss/', methods=['POST', 'GET'])
def get_department_area_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDepartmentAreaListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 创建部门区域
@app.route('/create_department_area_by_boss/', methods=['POST', 'GET'])
def create_department_area_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createDepartmentAreaByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 删除部门区域
@app.route('/delete_department_area_by_boss/', methods=['POST', 'GET'])
def delete_department_area_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deleteDepartmentAreaByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 获取指定部门区域
@app.route('/get_area_by_id_by_boss/', methods=['POST', 'GET'])
def get_area_by_id_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getAreaByIDByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 更新部门区域
@app.route('/update_department_area_name_by_boss/', methods=['POST', 'GET'])
def update_department_area_name_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.updateDepartmentAreaNameByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 部门区域树
@app.route('/get_area_tree_by_boss/', methods=['POST', 'GET'])
def get_area_tree_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getAreaTreeByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 设置权限
@app.route('/create_right_by_boss/', methods=['POST', 'GET'])
def create_right_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createRightByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 取消权限
@app.route('/delete_right_by_boss/', methods=['POST', 'GET'])
def delete_right_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deleteRightByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人上传标书
@app.route('/create_operation_bidding_book_by_boss/', methods=['POST', 'GET'])
def create_operation_bidding_book_by_boss():
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        bossManager = BossManager()
        (status, ret) = bossManager.createOperationBiddingBookByBoss(paramsJson, imgList)
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        if status is True:
            result['status'] = 'SUCCESS'
        result['data'] = ret
        return json.dumps(result)

#审核人推送消息
@app.route('/update_pushed_tender_by_auditor/', methods=['POST', 'GET'])
def update_pushed_tender_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.updatePushedTenderByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 批注正在进行中的项目
@app.route('/create_tender_comment_by_auditor/', methods=['POST', 'GET'])
def create_tender_comment_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.createTenderCommentByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 删除批注
@app.route('/delete_tender_comment_by_auditor/', methods=['POST', 'GET'])
def delete_tender_comment_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.deleteTenderCommentByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审核人 删除批注
@app.route('/get_all_data_info_by_auditor/', methods=['POST', 'GET'])
def get_all_data_info_by_auditor():
    auditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = auditorManager.getAllDataInfoByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取operation信息列表
@app.route('/get_operation_list_by_operator_id/', methods=['POST', 'GET'])
def get_operation_list_by_operator_id():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.getOperationListByOperatorID(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 由进行中 变为已完成
@app.route('/complete_pushed_tender_info/', methods=['POST', 'GET'])
def complete_pushed_tender_info():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.completePushedTenderInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 由已完成变为历史记录
@app.route('/update_to_history/', methods=['POST', 'GET'])
def update_to_history():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.updateToHistory(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 经办人获取我的推送数据分析
@app.route('/get_data_info_by_operator/', methods=['POST', 'GET'])
def get_data_info_by_operator():
    operatorManager = OperatorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = operatorManager.getDataInfoByOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 决定是否采用该经办人
@app.route('/validate_operator/', methods=['POST', 'GET'])
def validate_operator():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.validateOperator(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 决定是否采用该经办人
@app.route('/get_doing_detail_by_boss/', methods=['POST', 'GET'])
def get_doing_detail_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getDoingDetailByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#企业账号管理，成员列表
@app.route('/get_user_info_list_by_boss/', methods=['POST', 'GET'])
def get_user_info_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getUserInfoListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#企业账号管理，新建成员
@app.route('/create_user_info_by_boss/', methods=['POST', 'GET'])
def create_user_info_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.createUserInfoByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 企业账号管理，修改用户信息
@app.route('/update_user_info_by_boss/', methods=['POST', 'GET'])
def update_user_info_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.updateUserInfoByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人获取某个员工的信息
@app.route('/get_user_info_by_boss/', methods=['POST', 'GET'])
def get_user_info_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getUserInfoByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#企业账号管理，删除成员
@app.route('/delete_user_info_by_boss/', methods=['POST', 'GET'])
def delete_user_info_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.deleteUserInfoByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 审定人 分配经办人
@app.route('/update_operator_by_boss/', methods=['POST', 'GET'])
def update_operator_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.updateOperatorByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取资讯列表
@app.route('/get_news_list/', methods=['POST', 'GET'])
def get_news_list():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = newsManager.getNewsList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取资讯列表, 后台管理
@app.route('/get_news_list_background/', methods=['POST', 'GET'])
def get_news_list_background():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = newsManager.getNewsList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取资讯列表
@app.route('/get_news_detail/', methods=['POST', 'GET'])
def get_news_detail():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = newsManager.getNewsDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取资讯列表, 后台管理
@app.route('/get_news_detail_background/', methods=['POST', 'GET'])
def get_news_detail_background():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = newsManager.getNewsDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除资讯, 后台管理
@app.route('/delete_news_background/', methods=['POST', 'GET'])
def delete_news_background():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = newsManager.deleteNewsBackground(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建招标资讯
@app.route('/create_news/', methods=['POST', 'GET'])
def create_news():
    newsManager = NewsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        info = json.loads(paramsJson)
        imgNameList = info['imgNameList']
        imgList = []
        for img in imgNameList:
            _imgName = img['imgName']
            f = request.files[_imgName]
            imgName = f.filename
            imgDic = {}
            imgDic['imgName'] = imgName
            imgDic['file'] = f
            imgList.append(imgDic)
        (status, result) = newsManager.createNews(jsonInfo=paramsJson, imgFileList=imgList)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#审定人获取推送人员列表
@app.route('/get_tender_user_info_list_by_boss/', methods=['POST', 'GET'])
def get_tender_user_info_list_by_boss():
    bossManager = BossManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = bossManager.getTenderUserInfoListByBoss(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#审核人获取推送人员列表
@app.route('/get_tender_user_info_list_by_auditor/', methods=['POST', 'GET'])
def get_tender_user_info_list_by_auditor():
    aauditorManager = AuditorManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = aauditorManager.getTenderUserInfoListByAuditor(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取用户自己的详情
@app.route('/get_user_info_by_user_id/', methods=['POST', 'GET'])
def get_user_info_by_user_id():
    userBaseManager = UserBaseManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = userBaseManager.getUserInfoByUserID(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取公司资质等级列表
@app.route('/get_company_certificate_list/', methods=['POST', 'GET'])
def get_company_certificate_list():
    companyCertificateManager = CompanyCertificateManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = companyCertificateManager.getCompanyCertificateList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#创建订阅记录
@app.route('/create_subscribed_key/', methods=['POST', 'GET'])
def create_subscribed_key():
    subscribedKeyManager = SubscribedKeyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = subscribedKeyManager.createSubscribedKey(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取个人订阅信息
@app.route('/get_subscribe_info/', methods=['POST', 'GET'])
def get_subscribe_info():
    subscribedKeyManager = SubscribedKeyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = subscribedKeyManager.getSubscribeInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#==========================================
#微信公众号，自动回复接口
@app.route('/wx', methods=['POST', 'GET'])
def wx():
    wechatMessageManager = WechatMessageManager()
    wechatManager = WechatManager()
    if request.method == 'POST':
        xmlData = request.get_data()
        return wechatMessageManager.getMessageInfo(xmlData=xmlData)

    elif request.method == 'GET':
        paramsJson = {}
        paramsJson['signature'] = request.args.get('signature')
        paramsJson['timestamp'] = request.args.get('timestamp')
        paramsJson['nonce'] = request.args.get('nonce')
        paramsJson['echostr'] = request.args.get('echostr')
        paramsJson = json.dumps(paramsJson)
        (status, ret) = wechatManager.login(jsonInfo=paramsJson)
        return ret

#获取公众号人员列表
@app.route('/wx_get_user_info_list/', methods=['POST', 'GET'])
def wx_get_user_info_list():
    wechatManager = WechatManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = wechatManager.wxGetUserInfoList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


#小程序使用，获取我的订阅列表
@app.route('/get_wechat_subscribe_list/', methods=['POST', 'GET'])
def get_wechat_subscribe_list():
    subscribedKeyManager = SubscribedKeyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = subscribedKeyManager.getWeChatSubscribeList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 获取sts token
@app.route('/get_sts_token_info/', methods=['POST', 'GET'])
def get_sts_token_info():
    stsTokenManager = StsTokenManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = stsTokenManager.getStsTokenInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 用户获取文件列表
@app.route('/get_file_list_by_user/', methods=['POST', 'GET'])
def get_file_list_by_user():
    fileInfoManager = FileInfoManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = fileInfoManager.getFileListByUser(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 用户上传
@app.route('/create_file_info/', methods=['POST', 'GET'])
def create_file_info():
    fileInfoManager = FileInfoManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = fileInfoManager.createFileInfo(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 用户删除文件
@app.route('/delete_file_by_user/', methods=['POST', 'GET'])
def delete_file_by_user():
    fileInfoManager = FileInfoManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = fileInfoManager.deleteFileByUser(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取我的文件列表
@app.route('/get_my_file_list/', methods=['POST', 'GET'])
def get_my_file_list():
    fileInfoManager = FileInfoManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = fileInfoManager.getMyFileList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 重命名文件夹
@app.route('/rename_directory/', methods=['POST', 'GET'])
def rename_directory():
    fileInfoManager = FileInfoManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = fileInfoManager.renameDirectory(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

#创建自定义菜单
@app.route('/create_menu/', methods=['POST', 'GET'])
def create_menu():
    wechatManager = WechatManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = wechatManager.createMenu(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)


# 审定人 部门区域树
@app.route('/get_area_tree_withoud_user_id/', methods=['POST', 'GET'])
def get_area_tree_withoud_user_id():
    departmentAreaManager = DepartmentAreaManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = departmentAreaManager.getAreaTreeWithoutUserID(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建合同
@app.route('/create_contract/', methods=['POST', 'GET'])
def create_contract():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.createContract(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同列表
@app.route('/get_contract_list/', methods=['POST', 'GET'])
def get_contract_list():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.getContractList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同详情
@app.route('/get_contract_detail/', methods=['POST', 'GET'])
def get_contract_detail():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.getContractDetail(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同详情
@app.route('/delete_contract/', methods=['POST', 'GET'])
def delete_contract():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.deleteContract(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 编辑合同内容
@app.route('/update_contract/', methods=['POST', 'GET'])
def update_contract():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.updateContract(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 往合同中增加文件
@app.route('/add_file_to_contract/', methods=['POST', 'GET'])
def add_file_to_contract():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.addFileToContract(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除合同中的文件
@app.route('/delete_contract_file/', methods=['POST', 'GET'])
def delete_contract_file():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.deleteContractFile(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同文件列表
@app.route('/get_contract_file_list/', methods=['POST', 'GET'])
def get_contract_file_list():
    contractManager = ContractManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractManager.getContractFileList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建合同项目进度
@app.route('/create_contract_project_process/', methods=['POST', 'GET'])
def create_contract_project_process():
    contractProjectProcessManager = ContractProjectProcessManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractProjectProcessManager.createContractProjectProcess(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除合同项目进度
@app.route('/delete_contract_project_process/', methods=['POST', 'GET'])
def delete_contract_project_process():
    contractProjectProcessManager = ContractProjectProcessManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractProjectProcessManager.deleteContractProjectProcess(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同项目进度列表
@app.route('/get_contract_project_process_list/', methods=['POST', 'GET'])
def get_contract_project_process_list():
    contractProjectProcessManager = ContractProjectProcessManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractProjectProcessManager.getContractProjectProcessList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建合同决算
@app.route('/create_contract_final_account/', methods=['POST', 'GET'])
def create_contract_final_account():
    contractFinalAccountsManager = ContractFinalAccountsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractFinalAccountsManager.createContractFinalAccount(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除合同决算
@app.route('/delete_contract_final_account/', methods=['POST', 'GET'])
def delete_contract_final_account():
    contractFinalAccountsManager = ContractFinalAccountsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractFinalAccountsManager.deleteContractFinalAccount(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同决算列表
@app.route('/get_contract_final_account_list/', methods=['POST', 'GET'])
def get_contract_final_account_list():
    contractFinalAccountsManager = ContractFinalAccountsManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractFinalAccountsManager.getContractFinalAccountList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 创建合同突发事件
@app.route('/create_contract_emergency/', methods=['POST', 'GET'])
def create_contract_emergency():
    contractEmergencyManager = ContractEmergencyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractEmergencyManager.createContractEmergency(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 删除合同突发事件
@app.route('/delete_contract_emergency/', methods=['POST', 'GET'])
def delete_contract_emergency():
    contractEmergencyManager = ContractEmergencyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractEmergencyManager.deleteContractEmergency(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

# 获取合同突发事件列表
@app.route('/get_contract_emergency_list/', methods=['POST', 'GET'])
def get_contract_emergency_list():
    contractEmergencyManager = ContractEmergencyManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = contractEmergencyManager.getContractEmergencyList(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = result
        return json.dumps(data)

