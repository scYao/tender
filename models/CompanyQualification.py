# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CompanyQualification(db.Model):
    __tablename__ = 'CompanyQualification'

    joinID = db.Column(db.String(100), primary_key=True)
    companyID = db.Column(db.String(100))
    qualificationID = db.Column(db.String(100))

    def __init__(self, joinID=None, companyID=None, qualificationID=None):
        self.joinID = joinID
        self.companyID = companyID
        self.qualificationID = qualificationID

    def __repr__(self):
        return self.joinID