# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class SmsCode(db.Model):
    __tablename__ = 'SmsCode'

    codeID = db.Column(db.String(100), primary_key=True)
    tel = db.Column(db.String(20))
    code = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)

    def __init__(self, codeID=None, tel=None,
                 code=None, createTime=None):
        self.codeID = codeID
        self.tel = tel
        self.code = code
        self.createTime = createTime

    def __repr__(self):
        return self.codeID