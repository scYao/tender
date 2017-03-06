# coding=utf8
import os
import os.path
from flask import request
import sys

sys.path.append('..')
import json
from models.flask_app import app, cache

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



def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
@app.route('/find_password_with_sms_code/', methods=['POST', 'GET'])
def find_password_with_sms_code():
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
@app.route('/register_with_sms_code/', methods=['POST', 'GET'])
def register_with_sms_code():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        params = request.form['data']
        info = json.loads(params)
        info['ipAddress'] = request.headers['X-Forwarded-For']
        jsonInfo = json.dumps(info)
        (status, userID) = userManager.register(jsonInfo)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = userID

    return json.dumps(data)

# 获取收藏列表
@app.route('/get_favorite_list/', methods=['POST', 'GET'])
def get_favorite_list():
    favoriteManager = FavoriteManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, result) = favoriteManager.getFavoriteList(paramsJson)
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



