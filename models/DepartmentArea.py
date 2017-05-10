# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class DepartmentArea(db.Model):
    __tablename__ = 'DepartmentArea'
    areaID = db.Column(db.String(100), primary_key=True)
    areaName = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    departmentID = db.Column(db.String(100), db.ForeignKey('Department.departmentID'))

    def __init__(self, areaID=None, areaName=None,
                 createTime=None, departmentID=None):
        self.areaID = areaID
        self.areaName = areaName
        self.createTime = createTime
        self.departmentID = departmentID

    def __repr__(self):
        return self.areaID

    @staticmethod
    def generate(o):
        res = {}
        res['areaID'] = o.areaID
        res['areaName'] = o.areaName
        res['createTime'] = str(o.createTime)
        res['departmentID'] = o.departmentID
        return res