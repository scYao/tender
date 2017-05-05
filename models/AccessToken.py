# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class AccessToken(db.Model):
    __tablename__ = 'AccessToken'
    tokenID = db.Column(db.String(100), primary_key=True)
    accessTokenID = db.Column(db.String(200))
    createTime = db.Column(db.DateTime)
    validity = db.Column(db.Integer)

    def __init__(self, tokenID=None, accessTokenID=None, createTime=None, validity=None):
        self.tokenID = tokenID
        self.accessTokenID = accessTokenID
        self.createTime = createTime
        self.validity = validity

    def __repr__(self):
        return self.tokenID