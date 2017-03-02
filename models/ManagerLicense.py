# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class ManagerLicense(db.Model):
    __tablename__ = 'ManagerLicense'

    licenseID = db.Column(db.String(100), primary_key=True)
    licenseName = db.Column(db.String(100))
    licenseNum = db.Column(db.Integer)
    grade = db.Column(db.String(100))
    authority = db.Column(db.String(100))
    licenseDate = db.Column(db.Date)
    licenseEndDate = db.Column(db.Date)
    managerID = db.Column(db.String(100))
    tag = db.Column(db.Integer)


    def __init__(self, licenseID=None, licenseName=None, licenseNum=None,
                 grade=None, authority=None, licenseDate=None,
                 licenseEndDate=None, managerID=None, tag=None):
        self.licenseID = licenseID
        self.licenseName = licenseName
        self.licenseNum = licenseNum
        self.grade = grade
        self.authority = authority
        self.licenseDate = licenseDate
        self.licenseEndDate = licenseEndDate
        self.managerID = managerID
        self.tag = tag

    @staticmethod
    def generate(c):
        res = {}
        res['licenseID'] = c.licenseID
        res['licenseName'] = c.licenseName
        res['licenseNum'] = c.licenseNum
        res['grade'] = c.grade
        res['authority'] = c.authority
        res['licenseDate'] = c.licenseDate
        res['licenseEndDate'] = c.licenseEndDate
        res['managerID'] = c.managerID
        res['tag'] = c.tag
        return res

    def __repr__(self):
        return self.licenseID
