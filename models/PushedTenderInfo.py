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
    #进行中字段
    projectManagerName = db.Column(db.String(100))
    openedDate = db.Column(db.Date)
    openedLocation = db.Column(db.Text)
    ceilPrice = db.Column(db.Float)
    tenderInfoDescription = db.Column(db.Text)
    quotedPrice = db.Column(db.Float)
    quotedDate = db.Column(db.Date)
    quotedDescription = db.Column(db.Text)
    #已完成字段
    averagePrice = db.Column(db.Float)
    benchmarkPrice = db.Column(db.Float)
    K1 = db.Column(db.Float)
    K2 = db.Column(db.Float)
    Q1 = db.Column(db.Float)
    Q2 = db.Column(db.Float)
    deductedRate1 = db.Column(db.Float)
    deductedRate2 = db.Column(db.Float)
    workerName = db.Column(db.String(100))
    candidateName1 = db.Column(db.String(100))
    candidatePrice1 = db.Column(db.Float)
    candidateName2 = db.Column(db.String(100))
    candidatePrice2 = db.Column(db.Float)
    candidateName3 = db.Column(db.String(100))
    candidatePrice3 = db.Column(db.Float)

    def __init__(self, pushedID=None, userID=None, createTime=None,
                 responsiblePersonPushedTime=None, auditorPushedTime=None, state=0,
                 tenderID=None, step=0, projectManagerName='',
                 openedDate=None, openedLocation='', ceilPrice=0,
                 tenderInfoDescription='', quotedPrice=0, quotedDate=None,
                 quotedDescription='', averagePrice=0, benchmarkPrice=0,
                 K1=0, K2=0, Q1=0,
                 Q2=0, deductedRate1=0, deductedRate2=0,
                 workerName='', candidateName1='', candidatePrice1=0,
                 candidateName2='', candidatePrice2=0, candidateName3='',
                 candidatePrice3=0):
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
        self.averagePrice = averagePrice
        self.benchmarkPrice = benchmarkPrice
        self.K1 = K1
        self.K2 = K2
        self.Q1 = Q1
        self.Q2 = Q2
        self.deductedRate1 = deductedRate1
        self.deductedRate2 = deductedRate2
        self.workerName = workerName
        self.candidateName1 = candidateName1
        self.candidatePrice1 = candidatePrice1
        self.candidateName2 = candidateName2
        self.candidatePrice2 = candidatePrice2
        self.candidateName3 = candidateName3
        self.candidatePrice3 = candidatePrice3

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
            tenderID=info['tenderID']
            # projectManagerName=info['projectManagerName'],
            # openedDate=info['openedDate'],
            # openedLocation=info['openedLocation'],
            # ceilPrice=info['ceilPrice'],
            # tenderInfoDescription=info['tenderInfoDescription'],
            # quotedPrice=info['quotedPrice'],
            # quotedDate=info['quotedDate'],
            # quotedDescription=info['quotedDescription']
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
        res['openedDate'] = str(c.openedDate)
        res['openedLocation'] = c.openedLocation
        res['ceilPrice'] = c.ceilPrice
        res['tenderInfoDescription'] = c.tenderInfoDescription
        res['quotedPrice'] = c.quotedPrice
        res['quotedDate'] = str(c.quotedDate)
        res['quotedDescription'] = c.quotedDescription
        res['averagePrice'] = c.averagePrice
        res['benchmarkPrice'] = c.benchmarkPrice
        res['K1'] = c.K1
        res['K2'] = c.K2
        res['Q1'] = c.Q1
        res['Q2'] = c.Q2
        res['deductedRate1'] = c.deductedRate1
        res['deductedRate2'] = c.deductedRate2
        res['workerName'] = c.workerName
        res['candidateName1'] = c.candidateName1
        res['candidatePrice1'] = c.candidatePrice1
        res['candidateName2'] = c.candidateName2
        res['candidatePrice2'] = c.candidatePrice2
        res['candidateName3'] = c.candidateName3
        res['candidatePrice3'] = c.candidatePrice3
        return res

    def __repr__(self):
        return self.pushedID


