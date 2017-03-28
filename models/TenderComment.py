# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class TenderComment(db.Model):

    __tablename__ = 'TenderComment'
    commentID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    tenderID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    description = db.Column(db.Text)

    def __init__(self, commentID=None, userID=None, createTime=None,
                 description=None, tenderID=None):
        self.commentID = commentID
        self.userID = userID
        self.createTime = createTime
        self.description = description
        self.tenderID = tenderID

    @staticmethod
    def create(info):
        tenderComment = TenderComment(
            commentID=info['commentID'],
            userID=info['userID'],
            createTime=info['createTime'],
            description=info['description'],
            tenderID=info['tenderID']
        )
        db.session.add(tenderComment)
        return (True, info['commentID'])

    @staticmethod
    def generate(c):
        res = {}
        res['commentID'] = c.commentID
        res['userID'] = c.userID
        res['createTime'] = c.createTime
        res['description'] = c.description
        return res

    def __repr__(self):
        return self.commentID


