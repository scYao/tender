# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class StsToken(db.Model):
    __tablename__ = 'StsToken'
    tokenID = db.Column(db.String(100), primary_key=True)
    AccessKeySecret = db.Column(db.String(100))
    AccessKeyId = db.Column(db.String(100))
    Expiration = db.Column(db.DateTime)
    SecurityToken = db.Column(db.String(1000))
    createTime = db.Column(db.DateTime)

    def __init__(self, tokenID=None, AccessKeySecret=None,
                 AccessKeyId=None, Expiration=None,
                 SecurityToken=None, createTime=None):
        self.tokenID = tokenID
        self.AccessKeySecret = AccessKeySecret
        self.AccessKeyId = AccessKeyId
        self.Expiration = Expiration
        self.SecurityToken = SecurityToken
        self.createTime = createTime


    @staticmethod
    def generate(o):
        res = {}
        res['tokenID'] = o.tokenID
        res['AccessKeySecret'] = o.AccessKeySecret
        res['AccessKeyId'] = o.AccessKeyId
        res['Expiration'] = str(o.Expiration)
        res['SecurityToken'] = o.SecurityToken
        res['createTime'] = str(o.createTime)
        return res

    def __repr__(self):
        return self.tokenID