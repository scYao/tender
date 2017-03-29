# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db
from sqlalchemy.orm import relationship

class Message(db.Model):
    __tablename__ = 'Message'
    messageID = db.Column(db.String(100), primary_key=True)
    foreignID = db.Column(db.String(100))
    # merchandiseID = db.Column(db.String(100), db.ForeignKey('PostedMerchandise.merchandiseID'))
    # replyID = db.Column(db.String(100))
    fromUserID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    toUserID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    description = db.Column(db.Text)
    createTime = db.Column(db.DateTime)
    tag = db.Column(db.Integer)
    state = db.Column(db.Integer)

    fromUserID_FK = relationship("UserInfo", foreign_keys=[fromUserID])
    toUserID_FK = relationship("UserInfo", foreign_keys=[toUserID])

    def __init__(self, messageID=None, foreignID=None, fromUserID=None,
                 toUserID=None, description=None, createTime=None, tag=0,
                 state = False):
        self.messageID = messageID
        self.foreignID = foreignID
        self.fromUserID = fromUserID
        self.toUserID = toUserID
        self.description = description
        self.createTime = createTime
        self.tag = tag
        self.state = state

    def __repr__(self):
        return self.messageID

    @staticmethod
    def generate(o):
        res = {}
        res['messageID'] = o.messageID
        res['foreignID'] = o.foreignID
        res['fromUserID'] = o.fromUserID
        res['toUserID'] = o.toUserID
        res['description'] = o.description
        res['createTime'] = str(o.createTime)
        return res