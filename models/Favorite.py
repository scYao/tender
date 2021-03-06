# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Favorite(db.Model):
    __tablename__ = 'Favorite'
    favoriteID = db.Column(db.String(100), primary_key=True)
    createTime = db.Column(db.DateTime)
    tenderID = db.Column(db.String(100))
    tag = db.Column(db.String(100))
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))

    def __init__(self, favoriteID=None, createTime=None,
                 tenderID=None, userID=None, tag='tender'):
        self.favoriteID = favoriteID
        self.createTime = createTime
        self.tenderID = tenderID
        self.userID = userID
        self.tag = tag

    def __repr__(self):
        return self.favoriteID

    @staticmethod
    def generate(f):
        res = {}
        res['favoriteID'] = f.favoriteID
        res['favoriteCreateTime'] = str(f.createTime)
        res['tag'] = f.tag
        return res