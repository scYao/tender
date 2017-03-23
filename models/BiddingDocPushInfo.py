# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class BiddingDocPushInfo(db.Model):

    __tablename__ = 'BiddingDocPushInfo'
    pushedID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    responsiblePersonPushedTime = db.Column(db.DateTime)
    auditorPushedTime = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    tenderID = db.Column(db.String(100))

    def __init__(self, pushedID=None, userID=None, createTime=None,
                 responsiblePersonPushedTime=None, auditorPushedTime=None, state=0,
                 tenderID=None):
        self.pushedID = pushedID
        self.userID = userID
        self.createTime = createTime
        self.responsiblePersonPushedTime = responsiblePersonPushedTime
        self.auditorPushedTime = auditorPushedTime
        self.state = state
        self.tenderID = tenderID

    @staticmethod
    def create(info):
        biddingDocPushInfo = BiddingDocPushInfo(
            pushedID=info['pushedID'],
            userID=info['userID'],
            createTime=info['createTime'],
            responsiblePersonPushedTime=info['responsiblePersonPushedTime'],
            auditorPushedTime=info['auditorPushedTime'],
            state=info['state'],
            tenderID=info['tenderID'],
        )
        db.session.add(biddingDocPushInfo)
        return (True, info['pushedID'])

    @staticmethod
    def generate(c):
        res = {}
        res['pushedID'] = c.pushedID
        res['userID'] = c.userID
        res['createTime'] = c.createTime
        res['responsiblePersonPushedTime'] = c.responsiblePersonPushedTime
        res['auditorPushedTime'] = c.auditorPushedTime
        res['state'] = c.state
        res['tenderID'] = c.tenderID
        return res

    def __repr__(self):
        return self.pushedID


