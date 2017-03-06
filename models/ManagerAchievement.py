# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class ManagerAchievement(db.Model):
    __tablename__ = 'ManagerAchievement'

    achievementID = db.Column(db.String(100), primary_key=True)
    projectName = db.Column(db.String(100))
    companyName = db.Column(db.String(100))
    winBiddingDate = db.Column(db.Date)
    price = db.Column(db.Float)
    projectManagerName = db.Column(db.String(100))
    managerID = db.Column(db.String(100), db.ForeignKey('ProjectManager.managerID'))
    tag = db.Column(db.Integer)


    def __init__(self, achievementID=None, projectName=None, companyName=None,
                 winBiddingDate=None, price=0, projectManagerName=None,
                 managerID=None, tag=0):
        self.achievementID = achievementID
        self.projectName = projectName
        self.companyName = companyName
        self.winBiddingDate = winBiddingDate
        self.price = price
        self.projectManagerName = projectManagerName
        self.managerID = managerID
        self.tag = tag

    @staticmethod
    def generate(c):
        res = {}
        res['achievementID'] = c.achievementID
        res['projectName'] = c.projectName
        res['companyName'] = c.companyName
        res['winBiddingDate'] = c.winBiddingDate
        res['price'] = c.price
        res['projectManagerName'] = c.projectManagerName
        res['managerID'] = c.managerID
        res['tag'] = c.tag
        return res

    def __repr__(self):
        return self.achievementID
