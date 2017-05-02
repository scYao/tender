# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class AccessToken(db.Model):
    __tablename__ = 'AccessToken'
    accessTokenID = db.Column(db.String(200), primary_key=True)
    createTime = db.Column(db.DateTime)
    validity = db.Column(db.Integer)

    def __init__(self, accessTokenID=None, createTime=None, validity=None):
        self.accessTokenID = accessTokenID
        self.createTime = createTime
        self.validity = validity

    def __repr__(self):
        return self.accessTokenID