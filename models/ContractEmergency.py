# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class ContractEmergency(db.Model):

    __tablename__ = 'ContractEmergency'
    emergencyID = db.Column(db.String(100), primary_key=True)
    createTime = db.Column(db.DateTime)
    description = db.Column(db.Text)
    resolvent = db.Column(db.Text)
    contractID = db.Column(db.String(100), db.ForeignKey('Contract.contractID'))

    def __init__(self, emergencyID=None, createTime=None,
                 description=None, resolvent=None, contractID=None):
        self.emergencyID = emergencyID
        self.createTime = createTime
        self.description = description
        self.resolvent = resolvent
        self.contractID = contractID

    @staticmethod
    def generate(o):
        res = {}
        res['emergencyID'] = o.emergencyID
        if o.createTime is not None:
            res['createTime'] = str(o.createTime)[:10]
        else:
            res['createTime'] = ''
        res['description'] = o.description
        res['resolvent'] = o.resolvent
        res['contractID'] = o.contractID
        return res

    def __repr__(self):
        return self.emergencyID