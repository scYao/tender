# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db
from sqlalchemy.orm import relationship

class News(db.Model):
    __tablename__ = 'News'
    newsID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, newsID=None, title=None, content=None, createTime=None):
        self.newsID = newsID
        self.title = title
        self.content = content
        self.createTime = createTime

    @staticmethod
    def generate(o):
        res = {}
        res['newsID'] = o.newsID
        res['title'] = o.title
        res['content'] = o.content
        res['createTime'] = str(o.createTime)[0:10]
        return res

    @staticmethod
    def generateBrief(o):
        res = {}
        res['newsID'] = o.newsID
        res['title'] = o.title
        res['content'] = o.content
        res['createTime'] = str(o.createTime)[0:10]
        return res
