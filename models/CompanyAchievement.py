# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CompanyAchievement(db.Model):
    __tablename__ = 'CompanyAchievement'

    achievementID = db.Column(db.String(100), primary_key=True)
    projectName = db.Column(db.String(100))
    companyName = db.Column(db.String(100))
    winBiddingDate = db.Column(db.Date)
    price = db.Column(db.Float)
    projectManagerName = db.Column(db.String(100))
    managerID = db.Column(db.String(100))
    companyID = db.Column(db.String(100), db.ForeignKey('Company.companyID'))
    tag = db.Column(db.Integer)


    def __init__(self, achievementID=None, projectName=None, companyName=None,
                 winBiddingDate=None, price=0, projectManagerName=None,
                 managerID=None, companyID=None, tag=0):
        self.achievementID = achievementID
        self.projectName = projectName
        self.companyName = companyName
        self.winBiddingDate = winBiddingDate
        self.price = price
        self.projectManagerName = projectManagerName
        self.managerID = managerID
        self.companyID = companyID
        self.tag = tag

    @staticmethod
    def generate(o):
        res = {}
        res['achievementID'] = o.achievementID
        res['projectName'] = o.projectName
        res['companyName'] = o.companyName
        res['winBiddingDate'] = o.winBiddingDate
        res['price'] = o.price
        res['projectManagerName'] = o.projectManagerName
        res['managerID'] = o.managerID
        res['companyID'] = o.companyID
        res['tag'] = o.tag
        return res

    def __repr__(self):
        return self.achievementID
