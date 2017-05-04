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

    def __init__(self, pushedID=None, tenderID=None, toUserID=None, createTime=None):
        self.pushedID = pushedID
        self.tenderID = tenderID
        self.toUserID = toUserID
        self.createTime = createTime


    @staticmethod
    def create(createInfo):
        weChatPush = WeChatPush(
            pushedID=createInfo['pushedID'], tenderID=createInfo['tenderID'],
            toUserID=createInfo['toUserID'], createTime=createInfo['createTime']
        )
        db.session.add(weChatPush)
        return (True, None)

    def __repr__(self):
        return self.pushedID