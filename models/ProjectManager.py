# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class ProjectManager(db.Model):
    __tablename__ = 'ProjectManager'

    managerID = db.Column(db.String(100), primary_key=True)
    managerName = db.Column(db.String(100))
    gender = db.Column(db.Integer)
    positionalTitles = db.Column(db.String(100))
    post = db.Column(db.String(100))
    safetyAssessment = db.Column(db.String(100))
    safeEndDate = db.Column(db.Date)
    safeAuthority = db.Column(db.String(100))
    safeFromDate = db.Column(db.Date)
    companyID = db.Column(db.String(100), db.ForeignKey('Company.companyID'))

    projectManager = db.relationship('ManagerAchievement', backref='ProjectManager', lazy='dynamic')

    def __init__(self, managerID=None, managerName=None, gender=None,
                 positionalTitles=None, post=None,
                 safetyAssessment=None, safeEndDate=None, safeAuthority=None,
                 safeFromDate=None, companyID=None):
        self.managerID = managerID
        self.managerName = managerName
        self.gender = gender
        self.positionalTitles = positionalTitles
        self.post = post
        self.safetyAssessment = safetyAssessment
        self.safeEndDate = safeEndDate
        self.safeAuthority = safeAuthority
        self.safeFromDate = safeFromDate
        self.companyID = companyID

    @staticmethod
    def generate(c):
        res = {}
        res['managerID'] = c.managerID
        res['managerName'] = c.managerName
        res['gender'] = c.gender
        res['positionalTitles'] = c.positionalTitles
        res['post'] = c.post
        res['safetyAssessment'] = c.safetyAssessment
        res['safeEndDate'] = str(c.safeEndDate)
        res['safeAuthority'] = c.safeAuthority
        res['safeFromDate'] = str(c.safeFromDate)
        res['companyID'] = c.companyID
        return res

    def __repr__(self):
        return self.managerID
