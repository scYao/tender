# coding=utf8
import sys
import json
sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func

from models.flask_app import db
from models.UserInfo import UserInfo
from models.Token import Token
from models.SmsCode import SmsCode
from models.UserIP import UserIP
from tool.Util import Util
from tool.config import ErrorInfo
from tool.StringConfig import STRING_INFO_SMS_REGISTER

from stoken.TokenManager import TokenManager

class UserManager(Util):
    def __init__(self):
        pass

    def login(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = info['password']
        # 验证用户真实存在
        query = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        )
        result = query.first()
        if not result:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        # 验证登录密码正确
        passwordResult = query.filter(
            and_(UserInfo.tel == tel,
                 UserInfo.password == password)
        ).first()
        if not passwordResult:
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
        return (True, tokenID)

    def register(self, jsonInfo):
        info = json.loads(jsonInfo)
        # 验证码验证
        (status, reason) = self.checkSmsCode(info)
        if status is not True:
            return (False, reason)
        # 添加用户记录
        (status, createInfo) = self.__createUserInfo(info)
        # if status is not True:
        if status is not True:
            return (False, createInfo)
        # tel = resultData[3]
        userID = createInfo['userID']
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
        pwd = info['password']
        # ipAddress = info['ipAddress']
        portrait = info['portrait']
        gender = int(info['gender'])
        userName = info['userName']
        deviceID = info['deviceID']
        if portrait == '-1' and gender == 0:
            portrait = 'ladyPortrait.png'
        if portrait == '-1' and gender == 1:
            portrait = 'gentlemanPortrait.png'
        # 判断是否已经注册
        result = db.session.query(UserInfo).filter(
            UserInfo.tel == tel
        ).first()
        if result is not None:
            errorInfo = ErrorInfo['TENDER_07']
            errorInfo['detail'] = None
            return (False, errorInfo)

        # result = db.session.query(UserInfo).filter(
        #     UserInfo.deviceID == deviceID
        # ).first()
        # if result is not None:
        #     # 判断同一个设备是否已经注册过
        #     errorInfo = ErrorInfo['SPORTS_07']
        #     errorInfo['detail'] = None
        #     errorInfo['zhInfo'] = '同一设备只能注册一次！'
        #     return (False, errorInfo)

        # 添加用户信息
        userID = self.generateID(tel)
        createInfo = {}
        createInfo['userID'] = userID
        createInfo['userName'] = userName
        createInfo['portrait'] = portrait
        code = self.generateCode(tel)
        createTime = datetime.now()
        userInfo = UserInfo(
            userID=userID, userName=userName,
            password=pwd, portraitPath=portrait,
            tel=tel, createTime=createTime,
            deviceID=deviceID, gender=gender,
            code=code
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
        return (True, createInfo)

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
            errorInfo = ErrorInfo['SPORTS_27']
            errorInfo['detail'] = result['error']
            return (False, errorInfo)

        now = datetime.now()
        smsCode = SmsCode(codeID=codeID, tel=tel, code=code, createTime=now)
        db.session.add(smsCode)
        try:
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)