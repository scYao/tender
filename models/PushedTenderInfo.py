# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class PushedTenderInfo(db.Model):

    __tablename__ = 'PushedTenderInfo'
    pushedID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    responsiblePersonPushedTime = db.Column(db.DateTime)
    auditorPushedTime = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    step = db.Column(db.Integer)
    tenderID = db.Column(db.String(100))

    def __init__(self, pushedID=None, userID=None, createTime=None,
                 responsiblePersonPushedTime=None, auditorPushedTime=None, state=0,
                 tenderID=None, step=0):
        self.pushedID = pushedID
        self.userID = userID
        self.createTime = createTime
        self.responsiblePersonPushedTime = responsiblePersonPushedTime
        self.auditorPushedTime = auditorPushedTime
        self.state = state
        self.step = step
        self.tenderID = tenderID

    @staticmethod
    def create(info):
        pushedTenderInfo = PushedTenderInfo(
            pushedID=info['pushedID'],
            userID=info['userID'],
            createTime=info['createTime'],
            responsiblePersonPushedTime=info['responsiblePersonPushedTime'],
            auditorPushedTime=info['auditorPushedTime'],
            state=info['state'],
            step=info['step'],
            tenderID=info['tenderID'],
        )
        db.session.add(pushedTenderInfo)
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
        res['step'] = c.step
        res['tenderID'] = c.tenderID
        return res

    def __repr__(self):
        return self.pushedID


