# coding=utf8
import sys
import json
sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import hashlib
from sqlalchemy import and_, text, func, desc
import traceback
from tool.tagconfig import CUSTOMIZEDCOMPANYID, DEFAULT_PWD

from models.flask_app import db
from models.UserInfo import UserInfo
from models.Token import Token
from models.SmsCode import SmsCode
from models.UserIP import UserIP
from models.AdminInfo import AdminInfo
from tool.Util import Util
from tool.config import ErrorInfo
from tool.StringConfig import STRING_INFO_SMS_REGISTER

from stoken.TokenManager import TokenManager

class UserManager(Util):
    def __init__(self):
        pass

    #重新生成所有招标检索
    def reGenerateUserSearchIndex(self, jsonInfo):
        info = json.loads(jsonInfo)
        query = db.session.query(UserInfo)
        allResult = query.all()
        # allResult
        # 生成搜索记录
        def regenerateInfo(result):
            searchInfo = {}
            searchInfo['joinID'] = self.generateID(result.userID)
            searchInfo['companyName'] = result.companyName
            searchInfo['userID'] = result.userID
            searchInfo['tel'] = result.tel
            searchInfo['jobPosition'] = result.jobPosition
            searchInfo['userName'] = result.userName
            searchInfo['createTime'] = result.createTime
            (status, addSearchInfo) = UserInfoSearchKey.createSearchInfo(searchInfo)
        _ = [regenerateInfo(result) for result in allResult]
        db.session.commit()
        return (True, '111')

    def getUserListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        #获取tenderID列表
        query = db.session.query(UserInfo)
        info['query'] = query
        allResult = query.offset(startIndex).limit(pageCount).all()
        userInfoList = [UserInfo.generate(result) for result in allResult]
        countQuery = db.session.query(func.count(UserInfo.userID))
        count = countQuery.first()
        count = count[0]
        biddingResult = {}
        biddingResult['dataList'] = userInfoList
        biddingResult['count'] = count
        return (True, biddingResult)



    def login(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = info['password']
        # 验证用户真实存在
        query = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        )
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_10']
            return (False, errorInfo)
        # 验证登录密码正确
        password = self.getMD5String(password)
        passwordResult = query.filter(
            and_(UserInfo.tel == tel,
                 UserInfo.password == password)
        ).first()
        if passwordResult is None:
            errorInfo = ErrorInfo['TENDER_05']
            return (False, errorInfo)
        # 生成新的Token记录
        userID = result.userID
        createTime = datetime.now()
        tokenID = self.generateID(userID)
        try:
            db.session.query(Token).filter(
                Token.userID == userID
            ).delete(synchronize_session=False)
            token = Token(
                tokenID=tokenID, userID=userID,
                createTime=createTime, validity='7'
            )
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        resultDic = {}
        resultDic['tokenID'] = tokenID
        return (True, resultDic)

    def register(self, jsonInfo):
        info = json.loads(jsonInfo)
        # 验证码验证
        # (status, reason) = self.checkSmsCode(info)
        # if status is not True:
        #     return (False, reason)
        # 添加用户记录
        (status, userID) = self.__createUserInfo(info)
        if status is not True:
            return (False, userID)
        tokenManager = TokenManager()
        tokenID = tokenManager.createToken(userID)
        resultData = {}
        resultData['tokenID'] = tokenID
        return (True, resultData)

    def createAdminManager(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        # 验证码验证
        # (status, reason) = self.checkSmsCode(info)
        # if status is not True:
        #     return (False, reason)
        # 添加用户记录
        userID = self.generateID(tel)
        info['adminID'] = userID
        (status, result) = AdminInfo.create(info)
        if status is not True:
            return (False, result)
        db.session.commit()
        tokenManager = TokenManager()
        tokenID = tokenManager.createToken(userID)
        resultData = {}
        resultData['tokenID'] = tokenID
        return (True, resultData)

    # 校验验证码
    def checkSmsCode(self, info):
        tel = info['tel']
        code = info['code']
        now = datetime.now()
        result = db.session.query(SmsCode).filter(
            and_(SmsCode.tel == tel, SmsCode.code == code,
                 func.TIMESTAMPDIFF(text('MINUTE'), SmsCode.createTime, now) <= 5)
        ).first()

        if result is None:
            errorInfo = ErrorInfo['TENDER_06']
            errorInfo['detail'] = result
            return (False, errorInfo)
        return (True, None)

    # 创建用户记录(注册时候,生成)
    def __createUserInfo(self, info):
        tel = info['tel']
        password = info['password']
        userName = info['userName']
        companyName = info['companyName']
        jobPosition = info['jobPosition']
        # portrait = 'ladyPortrait.png'
        portrait = 'gentlemanPortrait.png'
        # 判断是否已经注册
        result = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        ).first()
        if result is not None:
            errorInfo = ErrorInfo['TENDER_07']
            errorInfo['detail'] = None
            return (False, errorInfo)
        # 添加用户信息
        userID = self.generateID(tel)
        createTime = datetime.now()
        password = self.getMD5String(password)
        userInfo = UserInfo(
            userID=userID, userName=userName, password=password,
            portraitPath=portrait, tel=tel, createTime=createTime,
            companyName=companyName, jobPosition=jobPosition
        )
        # 添加用户注册IP地址记录
        joinID = self.generateID(userID)
        ipAddress = info['ipAddress']
        userIP = UserIP(
            joinID=joinID, userID=userID,
            createTime=createTime, ipAddress=ipAddress
        )
        try:
            db.session.add(userInfo)
            db.session.add(userIP)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, userID)

    # 短信验证码
    def sendSMS(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        codeID = self.generateID(str(tel))
        code = '%d%d%d%d' % (random.randint(0, 9), random.randint(0, 9),
                             random.randint(0, 9), random.randint(0, 9))

        resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
                             auth=("api", "key-de1098f4b8e2ef73c44a2332ddbe9058"),
                             data={
                                 "mobile": tel,
                                 "message": STRING_INFO_SMS_REGISTER % code
                             }, timeout=3, verify=False)
        result = json.loads(resp.content)
        if result['msg'] != 'ok':
            errorInfo = ErrorInfo['TENDER_11']
            errorInfo['detail'] = result['error']
            return (False, errorInfo)

        now = datetime.now()
        smsCode = SmsCode(codeID=codeID, tel=tel, code=code, createTime=now)
        db.session.add(smsCode)
        try:
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)

    # 更新用户信息
    def updateUserInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userName = info['userName'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        jobPosition = info['jobPosition'].replace('\'', '\\\'').replace('\"', '\\\"')
        tel = info['tel'].replace('\'', '\\\'').replace('\"', '\\\"')
        try:
            db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).update({
                UserInfo.userName : userName,
                UserInfo.tel : tel,
                UserInfo.companyName : companyName,
                UserInfo.jobPosition : jobPosition
            },
                synchronize_session=False)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)

    # 获取用户详情
    def getUserInfoDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()

            if result is None:
                errorInfo = ErrorInfo['TENDER_09']
                return (False, errorInfo)

            userDetail = UserInfo.generate(userInfo=result)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, userDetail)

    # 获取用户详情,后台
    def getUserInfoDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        userID = info['userID']
        (status, myUserID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()

            if result is None:
                errorInfo = ErrorInfo['TENDER_09']
                return (False, errorInfo)

            userDetail = UserInfo.generate(userInfo=result)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, userDetail)

    # 找回密码接口, 不校验验证码
    def __resetPassWord(self, tel, pwd):
        userQuery = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        )
        result = userQuery.first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_10']
            return (False, errorInfo)

        try:
            userQuery.update(
                {
                    UserInfo.password: pwd
                },
                synchronize_session=False
            )
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)

    # 找回密码接口, 校验验证码
    def findPasswordWithSmsCode(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = info['password']
        password = self.getMD5String(password)
        (status, reason) = self.checkSmsCode(info)
        if status is not True:
            return (False, reason)
        (status, reason) = self.__resetPassWord(tel=tel, pwd=password)
        if status is not True:
            return (False, reason)

        return (True, None)

    @staticmethod
    def getUserInfoListByIDTuple(info):
        foreignIDTuple = info['foreignIDTuple']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        query = db.session.query(UserInfo).filter(
            UserInfo.userID.in_(foreignIDTuple)
        ).order_by(desc(UserInfo.createTime)).offset(startIndex).limit(pageCount)
        allResult = query.all()
        userInfoList = [UserInfo.generate(result) for result in allResult]
        return filter(None, userInfoList)

    # OA系统登录界面
    def oaLogin(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = info['password']
        # 验证用户真实存在
        query = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        )
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_10']
            return (False, errorInfo)
        # 验证登录密码正确
        password = self.getMD5String(password)
        passwordResult = query.filter(
            and_(UserInfo.tel == tel,
                 UserInfo.password == password)
        ).first()
        if passwordResult is None:
            errorInfo = ErrorInfo['TENDER_05']
            return (False, errorInfo)
        userType = result.userType

        # 生成新的Token记录
        userID = result.userID
        createTime = datetime.now()
        tokenID = self.generateID(userID)
        try:
            db.session.query(Token).filter(
                Token.userID == userID
            ).delete(synchronize_session=False)
            token = Token(
                tokenID=tokenID, userID=userID,
                createTime=createTime, validity='7'
            )
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        resultDic = {}
        resultDic['tokenID'] = tokenID
        resultDic['userType'] = userType
        return (True, resultDic)

    #获取OA用户列表
    def getOAUserInfoList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(UserInfo).filter(
                UserInfo.customizedCompanyID == CUSTOMIZEDCOMPANYID
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [UserInfo.generateOAInfo(result) for result in allResult]
            countQuery = db.session.query(
                func.count(UserInfo.userID)
            ).filter(
                UserInfo.customizedCompanyID == CUSTOMIZEDCOMPANYID
            )
            count = countQuery.first()
            count = count[0]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    #创建OA用户
    def createOAUserInfo(self, info):
        userName = info['userName'].replace('\'', '\\\'').replace('\"', '\\\"')
        tel = info['tel'].replace('\'', '\\\'').replace('\"', '\\\"')
        password = info['password']
        userID = self.generateID(userName)
        info['userID'] = userID
        info['customizedCompanyID'] = CUSTOMIZEDCOMPANYID
        info['tel'] = tel
        info['password'] = self.getMD5String(password)
        info['userType'] = info['userTypeID']
        info['jobNumber'] = info['jobNumber']
        info['createTime'] = datetime.now()
        try:
            #判断是否已经存在该员工
            query = db.session.query(UserInfo).filter(UserInfo.tel == tel)
            result = query.first()
            if result is not None:
                return (False, ErrorInfo['TENDER_07'])
            UserInfo.create(createInfo=info)
            db.session.commit()
            return (True, userID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def deleteOAUserInfo(self, info):
        selfUserID = info['selfUserID']
        userID = info['userID']

        try:

            # 1, 判空后 查询该用户是否时自己公司的
            # 身份校验交给上层
            selfResult = db.session.query(UserInfo).filter(
                UserInfo.userID == selfUserID
            ).first()
            selfCompanyID = selfResult.customizedCompanyID

            userQuery = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            )
            userResult = userQuery.first()
            if userResult is None:
                return (False, ErrorInfo['TENDER_23'])
            userCompanyID = userResult.customizedCompanyID
            if selfCompanyID != userCompanyID:
                return (False, ErrorInfo['TENDER_33'])
            # 2, 删除用户
            userQuery.delete()
            db.session.commit()
            return (True, userID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def updateOAUserInfo(self, info):
        pass