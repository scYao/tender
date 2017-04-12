# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db
from sqlalchemy.orm import relationship

class News(db.Model):
    __tablename__ = 'News'
    newID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, newID=None, title=None, content=None, createTime=None):
        self.newID = newID
        self.title = title
        self.content = content
        self.createTime = createTime

    @staticmethod
    def generate(o):
        res = {}
        res['newID'] = o.newID
        res['title'] = o.title
        res['content'] = o.content
        res['createTime'] = str(o.createTime)
        return res

    @staticmethod
    def generateBrief(o):
        res = {}
        res['newID'] = o.newID
        res['title'] = o.title
        res['createTime'] = str(o.createTime)
        return res
