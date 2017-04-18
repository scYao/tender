# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class TenderSlave(db.Model):
    __tablename__ = 'TenderSlave'
    tenderID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    biddingNum = db.Column(db.String(100))

    def __init__(self, tenderID=None, title=None, biddingNum=None):
        self.tenderID = tenderID
        self.title = title
        self.biddingNum = biddingNum

    def __repr__(self):
        return self.tenderID