# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class Operator(db.Model):

    __tablename__ = 'Operator'
    operatorID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    tenderID = db.Column(db.String(100))
    tag = db.Column(db.Integer)

    def __init__(self, operatorID=None, userID=None, tenderID=None, tag=0):
        self.operatorID = operatorID
        self.userID = userID
        self.tenderID = tenderID
        self.tag = tag

    @staticmethod
    def create(info):
        operator = Operator(
            operatorID=info['operatorID'],
            userID=info['userID'],
            tenderID=info['tenderID'],
            tag=info['tag'],
        )
        db.session.add(operator)
        return (True, info['operatorID'])

    @staticmethod
    def generate(c):
        res = {}
        res['operatorID'] = c.operatorID
        res['userID'] = c.userID
        res['tenderID'] = c.tenderID
        res['tag'] = c.tag
        return res

    def __repr__(self):
        return self.operatorID


