# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class UserIP(db.Model):
    __tablename__ = 'UserIP'

    joinID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    ipAddress = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)

    def __init__(self, joinID=None, userID=None,
                 ipAddress=None, createTime=None):
        self.joinID = joinID
        self.userID = userID
        self.ipAddress = ipAddress
        self.createTime = createTime

    def __repr__(self):
        return self.joinID