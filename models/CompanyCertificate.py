# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CompanyCertificate(db.Model):
    __tablename__ = 'CompanyCertificate'

    joinID = db.Column(db.String(100), primary_key=True)
    companyID = db.Column(db.String(100))
    qualificationID = db.Column(db.String(100))
    tag = db.Column(db.Integer)

    def __init__(self, joinID=None, companyID=None, qualificationID=None, tag=0):
        self.joinID = joinID
        self.companyID = companyID
        self.qualificationID = qualificationID
        self.tag = tag

    def __repr__(self):
        return self.joinID

    @staticmethod
    def generate(c):
        res = {}
        res['joinID'] = c.joinID
        res['companyID'] = c.companyID
        res['qualificationID'] = c.qualificationID
        if c.tag == 0:
            res['tag'] = '主项'
        else:
            res['tag'] = '增项'
        return res
