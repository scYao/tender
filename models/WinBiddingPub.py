# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class WinBiddingPub(db.Model):
    __tablename__ = 'WinBiddingPub'

    biddingID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    publicDate = db.Column(db.Date)
    biddingNum = db.Column(db.String(100))
    detail = db.Column(db.Text)

    delinquenentConduct = db.relationship('Candidate', backref='WinBiddingPub', lazy='dynamic')

    def __init__(self, biddingID=None, title=None, publicDate=None,
                 biddingNum=None, detail=None):
        self.biddingID = biddingID
        self.title = title
        self.publicDate = publicDate
        self.biddingNum = biddingNum
        self.detail = detail

    @staticmethod
    def generate(b):
        res = {}
        res['biddingID'] = b.biddingID
        res['title'] = b.title
        res['publicDate'] = b.publicDate
        res['biddingNum'] = b.biddingNum
        res['detail'] = b.detail
        return res


