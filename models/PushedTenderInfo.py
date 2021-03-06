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
    operatorPersonPushedTime = db.Column(db.DateTime)
    responsiblePersonPushedTime = db.Column(db.DateTime)
    responsiblePersonID = db.Column(db.String(100))
    auditorPushedTime = db.Column(db.DateTime)
    auditorID = db.Column(db.String(100))
    bossPushedTime = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    step = db.Column(db.Integer)
    tag = db.Column(db.Integer)
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
    tenderCompanyName = db.Column(db.String(100))
    projectType = db.Column(db.String(100))
    workContent = db.Column(db.String(100))
    deposit = db.Column(db.Float)
    planScore = db.Column(db.Float)
    tenderType = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    winbidding = db.Column(db.Boolean)
    tenderee = db.Column(db.Text)
    tenderProxy = db.Column(db.Text)
    tenderer = db.Column(db.Text)
    constructionLocation = db.Column(db.Text)
    plannedProjectDuration = db.Column(db.Text)
    answerDeadline = db.Column(db.Date)
    tenderDeadline = db.Column(db.Date)
    attender = db.Column(db.Text)
    companyAchievement = db.Column(db.Text)
    pmAchievement = db.Column(db.Text)



    def __init__(self, pushedID=None, userID=None, createTime=None, operatorPersonPushedTime=None,
                 responsiblePersonPushedTime=None, auditorPushedTime=None, bossPushedTime=None,
                 state=0, tenderID=None, step=0, projectManagerName='',
                 openedDate=None, openedLocation='', ceilPrice=0,
                 tenderInfoDescription='', quotedPrice=0, quotedDate=None,
                 quotedDescription='', averagePrice=0, benchmarkPrice=0,
                 K1=0, K2=0, Q1=0,
                 Q2=0, deductedRate1=0, deductedRate2=0,
                 workerName='', candidateName1='', candidatePrice1=0,
                 candidateName2='', candidatePrice2=0, candidateName3='',
                 candidatePrice3=0, tag=0, tenderCompanyName=None, projectType=None,
                 workContent=None, deposit=0, planScore=0, tenderType=None,
                 deadline=None, winbidding=False, tenderee=None, tenderProxy=None,
                 tenderer=None, constructionLocation=None, plannedProjectDuration=None,
                 answerDeadline=None, tenderDeadline=None, attender=None,
                 companyAchievement=None, pmAchievement=None, responsiblePersonID=None, auditorID=None):
        self.pushedID = pushedID
        self.userID = userID
        self.createTime = createTime
        self.operatorPersonPushedTime = operatorPersonPushedTime
        self.responsiblePersonPushedTime = responsiblePersonPushedTime
        self.responsiblePersonID = responsiblePersonID
        self.auditorPushedTime = auditorPushedTime
        self.auditorID = auditorID
        self.bossPushedTime = bossPushedTime
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
        self.tag = tag
        self.tenderCompanyName = tenderCompanyName
        self.projectType = projectType
        self.workContent = workContent
        self.deposit = deposit
        self.planScore = planScore
        self.tenderType = tenderType
        self.deadline = deadline
        self.winbidding = winbidding
        self.tenderee = tenderee
        self.tenderProxy = tenderProxy
        self.tenderer = tenderer
        self.constructionLocation = constructionLocation
        self.plannedProjectDuration = plannedProjectDuration
        self.answerDeadline = answerDeadline
        self.tenderDeadline = tenderDeadline
        self.attender = attender
        self.companyAchievement = companyAchievement
        self.pmAchievement = pmAchievement


    @staticmethod
    def create(info):
        if info.has_key('auditorID'):
            auditorID = info['auditorID']
        else:
            auditorID = None

        if info.has_key('responsiblePersonID'):
            responsiblePersonID = info['responsiblePersonID']
        else:
            responsiblePersonID = None

        pushedTenderInfo = PushedTenderInfo(
            pushedID=info['pushedID'],
            userID=info['userID'],
            createTime=info['createTime'],
            operatorPersonPushedTime=info['operatorPersonPushedTime'],
            responsiblePersonPushedTime=info['responsiblePersonPushedTime'],
            auditorPushedTime=info['auditorPushedTime'],
            bossPushedTime=info['bossPushedTime'],
            state=info['state'],
            step=info['step'],
            tenderID=info['tenderID'],
            tag=info['pushedTenderInfoTag'],
            deadline=info['deadline'],
            auditorID=auditorID,
            responsiblePersonID=responsiblePersonID
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
        if c.operatorPersonPushedTime is None:
            res['operatorPersonPushedTime'] = ''
        else:
            res['operatorPersonPushedTime'] = str(c.operatorPersonPushedTime)

        if c.responsiblePersonPushedTime is None:
            res['responsiblePersonPushedTime'] = ''
            res['responsiblePersonID'] = ''
        else:
            res['responsiblePersonPushedTime'] = str(c.responsiblePersonPushedTime)
            res['responsiblePersonID'] = c.responsiblePersonID

        if c.auditorPushedTime is None:
            res['auditorPushedTime'] = ''
            res['auditorID'] = ''
        else:
            res['auditorPushedTime'] = str(c.auditorPushedTime)
            res['auditorID'] = c.auditorID
        res['tenderID'] = c.tenderID
        res['state'] = c.state
        if c.deadline is None:
            res['deadline'] = ''
        else:
            res['deadline'] = str(c.deadline)
        res['tenderTag'] = c.tag
        return res

    @staticmethod
    def generate(c):
        res = {}
        res['pushedID'] = c.pushedID
        res['userID'] = c.userID
        res['operatorPersonPushedTime'] = str(c.operatorPersonPushedTime)
        res['responsiblePersonPushedTime'] = str(c.responsiblePersonPushedTime)
        res['auditorPushedTime'] = str(c.auditorPushedTime)
        res['state'] = c.state
        res['step'] = c.step
        res['tenderID'] = c.tenderID
        res['projectManagerName'] = c.projectManagerName
        res['openedDate'] = str(c.openedDate)
        res['openedLocation'] = c.openedLocation
        res['ceilPrice'] = c.ceilPrice==0 and ' ' or c.ceilPrice
        res['tenderInfoDescription'] = c.tenderInfoDescription
        res['quotedPrice'] = c.quotedPrice==0 and ' ' or c.quotedPrice
        res['quotedDate'] = str(c.quotedDate)
        res['quotedDescription'] = c.quotedDescription
        res['averagePrice'] = c.averagePrice==0 and ' ' or c.averagePrice
        res['benchmarkPrice'] = c.benchmarkPrice==0 and ' ' or c.benchmarkPrice
        res['K1'] = c.K1==0 and ' ' or c.K1
        res['K2'] = c.K2==0 and ' ' or c.K2
        res['Q1'] = c.Q1==0 and ' ' or c.Q1
        res['Q2'] = c.Q2==0 and ' ' or c.Q2
        res['deductedRate1'] = c.deductedRate1==0 and ' ' or c.deductedRate1
        res['deductedRate2'] = c.deductedRate2==0 and ' ' or c.deductedRate2
        res['workerName'] = c.workerName
        res['candidateName1'] = c.candidateName1
        res['candidatePrice1'] = c.candidatePrice1==0 and ' ' or c.candidatePrice1
        res['candidateName2'] = c.candidateName2
        res['candidatePrice2'] = c.candidatePrice2==0 and ' ' or c.candidatePrice2
        res['candidateName3'] = c.candidateName3
        res['candidatePrice3'] = c.candidatePrice3==0 and ' ' or c.candidatePrice3
        res['tenderCompanyName'] = c.tenderCompanyName
        res['projectType'] = c.projectType
        res['workContent'] = c.workContent
        res['deposit'] = c.deposit==0 and ' ' or c.deposit
        res['planScore'] = c.planScore
        res['tenderType'] = c.tenderType
        if c.deadline is None:
            res['deadline'] = ''
        else:
            res['deadline'] = str(c.deadline)
        res['winbidding'] = c.winbidding
        return res

    def __repr__(self):
        return self.pushedID


