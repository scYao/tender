# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class Operation(db.Model):

    __tablename__ = 'Operation'
    operationID = db.Column(db.String(100), primary_key=True)
    tag = db.Column(db.Integer)
    operatorID = db.Column(db.String(100))
    state = db.Column(db.Integer)
    description = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, operationID=None, tag=0, operatorID=None,
                 state=0, description=None, createTime=None):
        self.operationID = operationID
        self.tag = tag
        self.operatorID = operatorID
        self.state = state
        self.description = description
        self.createTime = createTime

    @staticmethod
    def create(info):
        operation = Operation(
            operationID=info['operationID'],
            tag=info['tag'],
            operatorID=info['operatorID'],
            state=info['state'],
            description=info['description'],
            createTime=info['createTime'],
        )
        db.session.add(operation)
        return (True, info['operationID'])

    @staticmethod
    def generate(c):
        res = {}
        res['operationID'] = c.operationID
        res['tag'] = c.tag
        res['operatorID'] = c.operatorID
        res['state'] = c.state
        res['description'] = c.description
        res['createTime'] = c.createTime
        return res

    def __repr__(self):
        return self.operationID


