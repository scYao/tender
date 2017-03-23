# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class CustomizedTender(db.Model):

    __tablename__ = 'CustomizedTender'
    tenderID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    createTime = db.Column(db.DateTime)
    userID = db.Column(db.String(100))
    url = db.Column(db.Text)

    def __init__(self, tenderID=None, title=None, createTime=None,
                 userID=None, url=None):
        self.tenderID = tenderID
        self.title = title
        self.createTime = createTime
        self.userID = userID
        self.url = url

    @staticmethod
    def create(info):
        customizedTender = CustomizedTender(
            tenderID=info['tenderID'],
            title=info['title'],
            createTime=info['createTime'],
            userID=info['userID'],
            url=info['url'],
        )
        db.session.add(customizedTender)
        return (True, info['tenderID'])

    @staticmethod
    def generate(c):
        res = {}
        res['tenderID'] = c.tenderID
        res['title'] = c.title
        res['createTime'] = c.createTime
        res['userID'] = c.userID
        res['url'] = c.url
        return res

    def __repr__(self):
        return self.tenderID


