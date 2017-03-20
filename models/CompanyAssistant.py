# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CompanyAssistant(db.Model):
    __tablename__ = 'CompanyAssistant'

    companyID = db.Column(db.String(100), primary_key=True)
    companyName = db.Column(db.String(100))
    foreignCompanyID = db.Column(db.String(100))

    def __init__(self, companyID=None, companyName=None, foreignCompanyID=None):
        self.companyID = companyID
        self.companyName = companyName
        self.foreignCompanyID = foreignCompanyID

    @staticmethod
    def generate(o):
        res = {}
        res['companyID'] = o.companyID
        res['companyName'] = o.companyName
        res['foreignCompanyID'] = o.foreignCompanyID
        return res