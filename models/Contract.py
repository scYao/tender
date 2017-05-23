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
    projectTypeID = db.Column(db.Integer)
    operationTypeID = db.Column(db.Integer)
    contractPrice = db.Column(db.Float)
    contractWorkContent = db.Column(db.String(1000))
    contractor = db.Column(db.String(1000))
    biddingDate = db.Column(db.DateTime)
    contractRecordDate = db.Column(db.DateTime)
    contractKeepingDeprt = db.Column(db.String(1000))
    archiveInfo = db.Column(db.String(1000))
    contractDuration = db.Column(db.String(1000))
    resultSubmissionDate = db.Column(db.String(100))
    resultReviewDate = db.Column(db.String(100))
    # submittalDate = db.Column(db.String(100))
    # submittalPrice = db.Column(db.Float)
    # authorizedPrice = db.Column(db.Float)
    # cumulativeInvoicePrice = db.Column(db.Float)
    # cumulativePayPrice = db.Column(db.Float)
    # balance = db.Column(db.Float)

    def __init__(self, contractID=None, title=None, serialNumber=None,
                 createTime=None, projectTypeID=0, operationTypeID=0,
                 contractPrice=0, contractWorkContent=None,
                 contractor=None, biddingDate=None, contractRecordDate=None,
                 contractKeepingDeprt=None, archiveInfo=None, contractDuration=None,
                 resultSubmissionDate=None, resultReviewDate=None):
        self.contractID = contractID
        self.title = title
        self.serialNumber = serialNumber
        self.createTime = createTime
        self.projectTypeID = projectTypeID
        self.operationTypeID = operationTypeID
        self.contractPrice = contractPrice
        self.contractWorkContent = contractWorkContent
        self.contractor = contractor
        self.biddingDate = biddingDate
        self.contractRecordDate = contractRecordDate
        self.contractKeepingDeprt = contractKeepingDeprt
        self.archiveInfo = archiveInfo
        self.contractDuration = contractDuration
        self.resultSubmissionDate = resultSubmissionDate
        self.resultReviewDate = resultReviewDate
        # self.submittalDate = submittalDate
        # self.submittalPrice = submittalPrice
        # self.authorizedPrice = authorizedPrice
        # self.cumulativeInvoicePrice = cumulativeInvoicePrice
        # self.cumulativePayPrice = cumulativePayPrice
        # self.balance = balance

    def __repr__(self):
        return self.contractID

    @staticmethod
    def generate(o):
        res = {}
        res['contractID'] = o.contractID
        res['title'] = o.title
        res['serialNumber'] = o.serialNumber
        res['createTime'] = str(o.createTime)
        res['projectTypeID'] = o.projectTypeID
        res['operationTypeID'] = o.operationTypeID
        res['contractPrice'] = o.contractPrice
        res['contractWorkContent'] = o.contractWorkContent
        res['contractor'] = o.contractor
        res['biddingDate'] = str(o.biddingDate)
        res['contractRecordDate'] = str(o.contractRecordDate)
        res['contractKeepingDeprt'] = o.contractKeepingDeprt
        res['archiveInfo'] = o.archiveInfo
        res['contractDuration'] = o.contractDuration
        res['resultSubmissionDate'] = o.resultSubmissionDate
        res['resultReviewDate'] = o.resultReviewDate
        # res['submittalDate'] = o.submittalDate
        # res['submittalPrice'] = o.submittalPrice
        # res['authorizedPrice'] = o.authorizedPrice
        # res['cumulativeInvoicePrice'] = o.cumulativeInvoicePrice
        # res['cumulativePayPrice'] = o.cumulativePayPrice
        # res['balance'] = o.balance

        return res
