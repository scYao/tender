# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class ContractProjectProcess(db.Model):

    __tablename__ = 'ContractProjectProcess'
    processID = db.Column(db.String(100), primary_key=True)
    createTime = db.Column(db.DateTime)
    processRate = db.Column(db.Integer)
    description = db.Column(db.Text)
    userName = db.Column(db.String(100))
    contractID = db.Column(db.String(100), db.ForeignKey('Contract.contractID'))

    def __init__(self, processID=None, createTime=None,
                 processRate=0, description=None, userName=None, contractID=None):
        self.processID = processID
        self.createTime = createTime
        self.processRate = processRate
        self.description = description
        self.userName = userName
        self.contractID = contractID


    @staticmethod
    def generate(o):
        res = {}
        res['processID'] = o.processID
        res['createTime'] = str(o.createTime)
        res['processRate'] = o.processRate
        res['description'] = o.description
        res['userName'] = o.userName
        res['contractID'] = o.contractID
        return res


    def __repr__(self):
        return self.processID