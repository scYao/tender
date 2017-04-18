# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class WinBiddingPubSlave(db.Model):
    __tablename__ = 'WinBiddingPubSlave'

    biddingID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    biddingNum = db.Column(db.String(100))


    def __init__(self, biddingID=None, title=None,
                 biddingNum=None):
        self.biddingID = biddingID
        self.title = title
        self.biddingNum = biddingNum

    def __repr__(self):
        return self.biddingID

