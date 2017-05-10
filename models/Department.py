# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Department(db.Model):
    __tablename__ = 'Department'
    departmentID = db.Column(db.String(100), primary_key=True)
    departmentName = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)


    def __init__(self, departmentID=None,
                 departmentName=None, createTime=None):
        self.departmentID = departmentID
        self.departmentName = departmentName
        self.createTime = createTime


    def __repr__(self):
        return self.departmentID

    @staticmethod
    def generate(o):
        res = {}
        res['departmentID'] = o.departmentID
        res['departmentName'] = o.departmentName
        res['createTime'] = str(o.createTime)
        return res
