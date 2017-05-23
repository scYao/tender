# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class ContractFinalAccounts(db.Model):

    __tablename__ = 'ContractFinalAccounts'
    accountID = db.Column(db.String(100), primary_key=True)
    submittalDate = db.Column(db.String(100))
    submittalPrice = db.Column(db.Float)
    authorizedPrice = db.Column(db.Float)
    cumulativeInvoicePrice = db.Column(db.Float)
    cumulativePayPrice = db.Column(db.Float)
    balance = db.Column(db.Float)
    contractID = db.Column(db.String(100), db.ForeignKey('Contract.contractID'))

    def __init__(self, accountID=None, submittalDate=None,
                 submittalPrice=0, authorizedPrice=0,
                 cumulativeInvoicePrice=0, cumulativePayPrice=0,
                 balance=0, contractID=None):
        self.accountID = accountID
        self.submittalDate = submittalDate
        self.submittalPrice = submittalPrice
        self.authorizedPrice = authorizedPrice
        self.cumulativeInvoicePrice = cumulativeInvoicePrice
        self.cumulativePayPrice = cumulativePayPrice
        self.balance = balance
        self.contractID = contractID

    @staticmethod
    def generate(o):
        res = {}
        res['accountID'] = o.accountID
        res['submittalDate'] = o.submittalDate
        res['submittalPrice'] = o.submittalPrice
        res['authorizedPrice'] = o.authorizedPrice
        res['cumulativeInvoicePrice'] = o.cumulativeInvoicePrice
        res['cumulativePayPrice'] = o.cumulativePayPrice
        res['balance'] = o.balance
        res['contractID'] = o.contractID
        return res

    def __repr__(self):
        return self.accountID