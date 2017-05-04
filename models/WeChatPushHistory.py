# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class WeChatPush(db.Model):
    __tablename__ = 'WeChatPush'
    pushedID = db.Column(db.String(100), primary_key=True)
    tenderID = db.Column(db.String(100))
    toUserID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    publishTime = db.Column(db.DateTime)

    def __init__(self, pushedID=None, tenderID=None,
                 toUserID=None, createTime=None,
                 publishTime=None):
        self.pushedID = pushedID
        self.tenderID = tenderID
        self.toUserID = toUserID
        self.createTime = createTime
        self.publishTime = publishTime

    def __repr__(self):
        return self.pushedID