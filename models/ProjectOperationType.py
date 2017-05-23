# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class ProjectOperationType(db.Model):

    __tablename__ = 'ProjectOperationType'
    operationTypeID = db.Column(db.Integer, primary_key=True)
    operationTypeName = db.Column(db.String(100))


    def __init__(self, operationTypeID=0, operationTypeName=None):
        self.operationTypeID = operationTypeID
        self.operationTypeName = operationTypeName


    def __repr__(self):
        return self.operationTypeID


    @staticmethod
    def generate(o):
        res = {}
        res['operationTypeID'] = o.operationTypeID
        res['operationTypeName'] = o.operationTypeName
        return res