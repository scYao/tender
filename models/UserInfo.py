# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

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
    cityID = db.Column(db.String(100), db.ForeignKey('City.cityID'))
    provinceID = db.Column(db.String(100), db.ForeignKey('Province.provinceID'))

    userIp = db.relationship('UserIP', backref='UserInfo', lazy='dynamic')

    def __init__(self, userID=None, userName=None, password=None,
                 info=None, portraitPath='default_portrait.png', account=0,
                 tel=None, email=None, gender=0,
                 createTime=None, deviceID=None, code=None,
                 cityID=63, provinceID=10):
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


    def __repr__(self):
        return self.userID

    @staticmethod
    def generate(userInfo):
        res = {}
        res['userID'] = userInfo.userID
        res['userName'] = userInfo.userName
        res['portraitPath'] = userInfo.portraitPath
        res['info'] = userInfo.info
        return res