# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class DepartmentRight(db.Model):
    __tablename__ = 'DepartmentRight'
    rightID = db.Column(db.String(100), primary_key=True)
    areaID = db.Column(db.String(100))
    userID = db.Column(db.String(100))
    tag = db.Column(db.Integer)



    def __init__(self, rightID=None, areaID=None,
                 userID=None, tag=0):
        self.rightID = rightID
        self.areaID = areaID
        self.userID = userID
        self.tag = tag

    def __repr__(self):
        return self.rightID


    @staticmethod
    def generate(o):
        res = {}
        res['rightID'] = o.rightID
        res['areaID'] = o.areaID
        res['userID'] = o.userID
        res['tag'] = o.tag
        return res