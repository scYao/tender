# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db
from tool.Util import Util
from tool.tagconfig import USER_TAG_DIC

class UserInfo(db.Model):
    __tablename__ = 'UserInfo'
    userID = db.Column(db.String(100), primary_key=True)
    userName = db.Column(db.String(100))
    password = db.Column(db.String(100))
    info = db.Column(db.Text)
    portraitPath = db.Column(db.Text)
    account = db.Column(db.Float)
    tel = db.Column(db.String(20))
    email = db.Column(db.String(100))
    deviceID = db.Column(db.String(100))
    gender = db.Column(db.Integer)
    createTime = db.Column(db.DateTime)
    code = db.Column(db.String(100))
    companyName = db.Column(db.String(100))
    jobPosition = db.Column(db.String(100))
    cityID = db.Column(db.String(100), db.ForeignKey('City.cityID'))
    provinceID = db.Column(db.String(100), db.ForeignKey('Province.provinceID'))
    customizedCompanyID = db.Column(db.String(100))
    userType = db.Column(db.Integer)
    jobNumber = db.Column(db.String(100))
    openid1 = db.Column(db.String(100))
    openid2 = db.Column(db.String(100))
    openid3 = db.Column(db.String(100))
    unionid = db.Column(db.String(100))
    disable = db.Column(db.Boolean)

    userIp = db.relationship('UserIP', backref='UserInfo', lazy='dynamic')

    def __init__(self, userID=None, userName=None, password=None,
                 info=None, portraitPath='default_portrait.png', account=0,
                 tel=None, email=None, gender=0,
                 createTime=None, deviceID=None, code=None,
                 cityID=63, provinceID=10, companyName=None, jobPosition=None,
                 customizedCompanyID=None, userType=0, jobNumber=None,
                 openid1=None, openid2=None, openid3=None,
                 unionid=None, disable=False):
        self.userID = userID
        self.userName = userName
        self.password = password
        self.info = info
        self.portraitPath = portraitPath
        self.account = account
        self.tel = tel
        self.email = email
        self.gender = gender
        self.createTime = createTime
        self.deviceID = deviceID
        self.code = code
        self.cityID = cityID
        self.provinceID = provinceID
        self.companyName = companyName
        self.jobPosition = jobPosition
        self.customizedCompanyID = customizedCompanyID
        self.userType = userType
        self.jobNumber = jobNumber
        self.openid1 = openid1
        self.openid2 = openid2
        self.openid3 = openid3
        self.unionid = unionid
        self.disable = disable

    def __repr__(self):
        return self.userID

    @staticmethod
    def generate(userInfo):
        util = Util()
        ossImgInfo = {}
        ossImgInfo['bucket'] = 'sjsecondhand'
        res = {}
        res['userID'] = userInfo.userID
        res['userName'] = userInfo.userName
        ossImgInfo['objectKey'] = 'portrait/%s' % userInfo.portraitPath
        res['portraitPath'] = util.getSecurityUrl(ossImgInfo)
        res['info'] = userInfo.info
        res['companyName'] = userInfo.companyName
        res['jobPosition'] = userInfo.jobPosition
        res['tel'] = userInfo.tel
        res['customizedCompanyID'] = userInfo.customizedCompanyID
        res['userType'] = userInfo.userType
        res['userTypeName'] = USER_TAG_DIC[userInfo.userType]
        res['jobNumber'] = userInfo.jobNumber
        res['disable'] = userInfo.disable
        return res

    @staticmethod
    def generateBrief(userInfo):
        res = {}
        res['userID'] = userInfo.userID
        res['userName'] = userInfo.userName
        res['jobNumber'] = userInfo.jobNumber
        return res

    @staticmethod
    def generateOAInfo(userInfo):
        res = {}
        res['userID'] = userInfo.userID
        res['userName'] = userInfo.userName
        res['userType'] = userInfo.userType
        res['userTypeName'] = USER_TAG_DIC[userInfo.userType]
        res['tel'] = userInfo.tel
        res['jobNumber'] = userInfo.jobNumber
        res['disable'] = userInfo.disable
        return res

    @staticmethod
    def create(createInfo):
        userInfo = UserInfo(
            userID=createInfo['userID'], userName=createInfo['userName'],
            tel=createInfo['tel'], userType=createInfo['userType'],
            customizedCompanyID=createInfo['customizedCompanyID'],
            password=createInfo['password'], createTime=createInfo['createTime'],
            jobNumber=createInfo['jobNumber']
        )
        db.session.add(userInfo)
        return (True, None)

    @staticmethod
    def createPublic(createInfo):
        userInfo = UserInfo(
            userID=createInfo['userID'], userName=createInfo['userName'],
            tel=createInfo['tel'], createTime=createInfo['createTime'],
            openid1=createInfo['openid1'], unionid = createInfo['unionid']
        )
        db.session.add(userInfo)
        return (True, None)

    @staticmethod
    def createApplet(createInfo):
        userInfo = UserInfo(
            userID=createInfo['userID'], userName=createInfo['userName'],
            tel=createInfo['tel'], createTime=createInfo['createTime'],
            openid2=createInfo['openid2'], unionid=createInfo['unionid']
        )
        db.session.add(userInfo)
        return (True, None)

    @staticmethod
    def createWeChat(createInfo):
        userInfo = UserInfo(
            userID=createInfo['userID'], userName=createInfo['userName'],
            tel=createInfo['tel'], createTime=createInfo['createTime'],
            openid1=createInfo['openid1'],openid2=createInfo['openid2'],
            unionid = createInfo['unionid'],
        )
        db.session.add(userInfo)
        return (True, None)