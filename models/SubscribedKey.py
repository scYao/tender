# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class SubscribedKey(db.Model):
    __tablename__ = 'SubscribedKey'
    subscribedID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    keywords = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    frequency = db.Column(db.Integer)
    pushType = db.Column(db.Integer)


    def __init__(self, subscribedID=None, userID=None,
                 keywords=None, createTime=None,
                 frequency=0, pushType=0):
        self.subscribedID = subscribedID
        self.userID = userID
        self.keywords = keywords
        self.createTime = createTime
        self.frequency = frequency
        self.pushType = pushType

    @staticmethod
    def generate(o):
        res = {}
        res['subscribedID'] = o.subscribedID
        res['userID'] = o.userID
        res['keywords'] = o.keywords
        res['createTime'] = o.createTime
        res['frequency'] = o.frequency
        res['pushType'] = o.pushType
        return res