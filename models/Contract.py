# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class Contract(db.Model):

    __tablename__ = 'Contract'
    contractID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(1000))
    serialNumber = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    projectTypeName = db.Column(db.Integer)
    operationTypeName = db.Column(db.Integer)
    contractPrice = db.Column(db.Float)
    contractWorkContent = db.Column(db.String(1000))
    contractor = db.Column(db.String(1000))
    responsiblePerson = db.Column(db.String(1000))
    biddingDate = db.Column(db.DateTime)
    contractRecordDate = db.Column(db.DateTime)
    contractKeepingDeprt = db.Column(db.String(1000))
    archiveInfo = db.Column(db.String(1000))
    contractDuration = db.Column(db.String(1000))

    def __init__(self, contractID=None, title=None, serialNumber=None,
                 createTime=None, projectTypeName=0, operationTypeName=0,
                 contractPrice=0, contractWorkContent=None,
                 contractor=None, responsiblePerson=None, biddingDate=None, contractRecordDate=None,
                 contractKeepingDeprt=None, archiveInfo=None, contractDuration=None):
        self.contractID = contractID
        self.title = title
        self.serialNumber = serialNumber
        self.createTime = createTime
        self.projectTypeName = projectTypeName
        self.operationTypeName = operationTypeName
        self.contractPrice = contractPrice
        self.contractWorkContent = contractWorkContent
        self.contractor = contractor
        self.responsiblePerson = responsiblePerson
        self.biddingDate = biddingDate
        self.contractRecordDate = contractRecordDate
        self.contractKeepingDeprt = contractKeepingDeprt
        self.archiveInfo = archiveInfo
        self.contractDuration = contractDuration

    def __repr__(self):
        return self.contractID

    @staticmethod
    def generate(o):
        res = {}
        res['contractID'] = o.contractID
        res['title'] = o.title
        res['serialNumber'] = o.serialNumber
        res['createTime'] = str(o.createTime)[:10]
        res['projectTypeName'] = o.projectTypeName
        res['operationTypeName'] = o.operationTypeName
        res['contractPrice'] = o.contractPrice
        res['contractWorkContent'] = o.contractWorkContent
        res['contractor'] = o.contractor
        res['responsiblePerson'] = o.responsiblePerson
        res['biddingDate'] = str(o.biddingDate)[:10]
        res['contractRecordDate'] = str(o.contractRecordDate)[:10]
        res['contractKeepingDeprt'] = o.contractKeepingDeprt
        res['archiveInfo'] = o.archiveInfo
        res['contractDuration'] = o.contractDuration

        return res
