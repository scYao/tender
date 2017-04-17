# coding=utf8
import base64
import sys
import json
import urllib
import urllib2

from Crypto.Cipher import AES

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import hashlib
from sqlalchemy import and_, text, func, desc
import traceback
from tool.tagconfig import CUSTOMIZEDCOMPANYID, DEFAULT_PWD, USER_TAG_BOSS, USER_TAG_OPERATOR
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from models.flask_app import db
from models.UserInfo import UserInfo
from models.Token import Token
from models.SmsCode import SmsCode
from models.UserIP import UserIP
from models.AdminInfo import AdminInfo
from models.PushedTenderInfo import PushedTenderInfo
from tool.Util import Util
from tool.config import ErrorInfo
from tool.StringConfig import STRING_INFO_SMS_REGISTER

from stoken.TokenManager import TokenManager

class UserManager(Util):
    def __init__(self):
        self.appID = 'wxc9029ba1dcf6f2de'
        self.appSecret = '7aba62050624812ba861146750e40de4'

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

        if userType<USER_TAG_BOSS or userType>USER_TAG_OPERATOR:
            return (False, ErrorInfo['TENDER_34'])

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


    # 获取OA用户列表
    def getOAUserInfoList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(UserInfo).filter(
                UserInfo.customizedCompanyID == CUSTOMIZEDCOMPANYID
            )
            allResult = query.order_by(desc(UserInfo.createTime)
                                       ).offset(startIndex).limit(pageCount).all()
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

    # 获取推送人员列表
    def getTenderUserInfoList(self, info):
        userType = info['userType']
        try:
            query = db.session.query(UserInfo).filter(
                and_(
                    UserInfo.customizedCompanyID == info['customizedCompanyID'],
                    UserInfo.userType >= userType
                )
            )
            if info.has_key('startIndex'):
                startIndex = info['startIndex']
                pageCount = info['pageCount']
                query = query.order_by(
                    desc(UserInfo.createTime)
                ).offset(startIndex).limit(pageCount)
            allResult = query.all()
            dataList = [UserInfo.generateOAInfo(result) for result in allResult]
            countQuery = db.session.query(
                func.count(UserInfo.userID)
            ).filter(
                and_(
                    UserInfo.customizedCompanyID == CUSTOMIZEDCOMPANYID,
                    UserInfo.userType >= userType
                )
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
        # info['customizedCompanyID'] = CUSTOMIZEDCOMPANYID
        info['tel'] = tel
        info['password'] = self.getMD5String(password)
        info['userType'] = info['userTypeID']
        info['jobNumber'] = info['jobNumber']
        info['createTime'] = datetime.now()
        try:
            # 获取boss的公司ID
            bossUserID = info['bossUserID']
            bossResult = db.session.query(UserInfo).filter(
                UserInfo.userID == bossUserID
            ).first()
            if bossResult is None:
                return (False, ErrorInfo['TENDER_07'])
            customizedCompanyID = bossResult.customizedCompanyID
            info['customizedCompanyID'] = customizedCompanyID
            #判断是否已经存在该员工
            query = db.session.query(UserInfo).filter(UserInfo.tel == tel)
            result = query.first()
            if result is not None:
                # 如果用户已存在 判断用户的公司是否是0
                customizedCompanyID = result.customizedCompanyID
                if customizedCompanyID != 0:
                    return (False, ErrorInfo['TENDER_37'])
                query.update({
                    UserInfo.customizedCompanyID : customizedCompanyID
                }, synchronize_session=False)
                # return (False, ErrorInfo['TENDER_07'])
            else:
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
            # 2.1 删除userIP信息
            db.session.query(UserIP).filter(
                UserIP.userID == userID
            ).delete(synchronize_session=False)
            # 2.2 删除pushedTenderInfo
            db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.userID == userID
            ).delete(synchronize_session=False)
            userQuery.delete(synchronize_session=False)
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


    # 使用微信账号登录
    def loginWithWechat(self, jsonInfo):
        info = json.loads(jsonInfo)
        #第一步：获取参数code, encryptedData, rawData, signature, iv
        code = info['code']
        encryptedData = info['encryptedData']
        rawData = info['rawData']
        rawData = str(rawData)
        signature = info['signature']
        iv = info['iv']
        #第二步：　获取唯一的openid, session_key
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s' \
              '&secret=%s&js_code=%s&grant_type=authorization_code' % (self.appID, self.appSecret, code)
        f = urllib.urlopen(url)
        ret = json.loads(f.read())
        #判断是否获取成功
        if(len(ret['session_key']) > 1 and len(ret['openid']) > 1):
            #第三步：根据openid, 生成tokenID, 将tokenID, session_key 存入到数据库中
            openID = ret['openid']
            sessionKey = ret['session_key']
            sessionKey = str(sessionKey)
            #第四步，　验证签名
            newSignature = hashlib.sha1(rawData + sessionKey).hexdigest()
            if(newSignature == signature):
                encryptedData = encryptedData.encode('utf-8')
                resultDict = self.decrypt(encryptedData, iv, sessionKey)
                tokenManager = TokenManager()
                tokenID = tokenManager.createToken(openID)
                # db.session.query(Token).filter(
                #     Token.tokenID == tokenID
                # ).update({Token.sessionKey: sessionKey}, synchronize_session=False)
                #查询是否存在已经创建的用户
                allResult = db.session.query(UserInfo).filter(UserInfo.userID == openID).all()
                if(len(allResult) < 1):
                    now = datetime.now()
                    uInfo = {}
                    uInfo['url'] = resultDict['avatarUrl']
                    uInfo['userName'] = resultDict['nickName']
                    userInfo = UserInfo(userID=openID, userName=resultDict['nickName'],
                                        gender=resultDict['gender'], createTime=now)
                    db.session.add(userInfo)

                db.session.commit()
                resultDict['tokenID'] = tokenID
                return (True, tokenID)
        else:
            return (False, None)


    #微信登录时候，解密用户加密的数据信息
    def decrypt(self, encryptedData, iv, sessionKey):
        # base64 decode
        sessionKey = base64.b64decode(sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)
        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        if decrypted['watermark']['appid'] != self.appID:
            raise Exception('Invalid Buffer')
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


    # 获取经办人 审核人 审定人 信息
    def getStaffInfo(self, info):
        customizedCompanyID = info['customizedCompanyID']
        userType = info['userType']
        try:
            result = db.session.query(UserInfo).filter(
                and_(
                    UserInfo.userType == userType,
                    UserInfo.customizedCompanyID == customizedCompanyID
                )
            ).first()
            if result is None:
                return (False, ErrorInfo['TENDER_23'])
            resp = {}
            resp['userID'] = result.userID
            resp['userName'] = result.userName
            resp['userType'] = result.userType
            return (True, resp)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getUserInfo(self, info):
        userID = info['userID']

        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
            if result is None:
                return (False, ErrorInfo['TENDER_23'])
            return (True, UserInfo.generate(userInfo=result))
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)