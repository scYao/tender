# coding=utf8
import os
import os.path
from flask import request
import sys

sys.path.append('..')
import json
from models.flask_app import app, cache
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
from projectManager.PMManager import PMManager
from projectManager.LicenseManager import LicenseManager
from projectManager.AchievementManager import AchievementManager
from certificationGrade.CertificationGrade1Manager import CertificationGrade1Manager
from certificationGrade.CertificationGrade2Manager import CertificationGrade2Manager
from certificationGrade.CertificationGrade3Manager import CertificationGrade3Manager
from certificationGrade.CertificationGrade4Manager import CertificationGrade4Manager
from winBidding.WinBiddingManager import WinBiddingManager
from winBidding.CandidateManager import CandidateManager
from search.SearchManager import SearchManager
from image.ImageManager import ImageManager


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

# 获取中标信息列表
@app.route('/get_bid_list/', methods=['POST', 'GET'])
def get_bid_list():
    winBiddingManager = WinBiddingManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = winBiddingManager.getBidList(paramsJson)
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
    achievementManager = AchievementManager()
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
        (status, result) = searchManager.search(paramsJson)
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




