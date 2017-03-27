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
    projectManagerName = db.Column(db.String(100))
    openedDate = db.Column(db.Date)
    openedLocation = db.Column(db.Text)
    ceilPrice = db.Column(db.Float)
    tenderInfoDescription = db.Column(db.Text)
    quotedPrice = db.Column(db.Float)
    quotedDate = db.Column(db.Date)
    quotedDescription = db.Column(db.Text)

    def __init__(self, pushedID=None, userID=None, createTime=None,
                 responsiblePersonPushedTime=None, auditorPushedTime=None, state=0,
                 tenderID=None, step=0, projectManagerName=None,
                 openedDate=None, openedLocation=None, ceilPrice=0,
                 tenderInfoDescription=None, quotedPrice=0, quotedDate=None,
                 quotedDescription=None):
        self.pushedID = pushedID
        self.userID = userID
        self.createTime = createTime
        self.responsiblePersonPushedTime = responsiblePersonPushedTime
        self.auditorPushedTime = auditorPushedTime
        self.state = state
        self.step = step
        self.tenderID = tenderID
        self.projectManagerName = projectManagerName
        self.openedDate = openedDate
        self.openedLocation = openedLocation
        self.ceilPrice = ceilPrice
        self.tenderInfoDescription = tenderInfoDescription
        self.quotedPrice = quotedPrice
        self.quotedDate = quotedDate
        self.quotedDescription = quotedDescription

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
            projectManagerName=info['projectManagerName'],
            openedDate=info['openedDate'],
            openedLocation=info['openedLocation'],
            ceilPrice=info['ceilPrice'],
            tenderInfoDescription=info['tenderInfoDescription'],
            quotedPrice=info['quotedPrice'],
            quotedDate=info['quotedDate'],
            quotedDescription=info['quotedDescription']
        )
        db.session.add(pushedTenderInfo)
        return (True, info['pushedID'])

    @staticmethod
    def generateBrief(c):
        res = {}
        res['pushedID'] = c.pushedID
        res['createTime'] = str(c.createTime)
        res['tenderID'] = c.tenderID
        res['state'] = c.state
        return res

    @staticmethod
    def generate(c):
        res = {}
        res['pushedID'] = c.pushedID
        res['userID'] = c.userID
        res['createTime'] = str(c.createTime)
        res['responsiblePersonPushedTime'] = str(c.responsiblePersonPushedTime)
        res['auditorPushedTime'] = str(c.auditorPushedTime)
        res['state'] = c.state
        res['step'] = c.step
        res['tenderID'] = c.tenderID
        res['projectManagerName'] = c.projectManagerName
        res['openedDate'] = c.openedDate
        res['openedLocation'] = c.openedLocation
        res['ceilPrice'] = c.ceilPrice
        res['tenderInfoDescription'] = c.tenderInfoDescription
        res['quotedPrice'] = c.quotedPrice
        res['quotedDate'] = c.quotedDate
        res['quotedDescription'] = c.quotedDescription
        return res

    def __repr__(self):
        return self.pushedID


