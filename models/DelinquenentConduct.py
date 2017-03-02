# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class DelinquenentConduct(db.Model):
    __tablename__ = 'DelinquenentConduct'

    conductID = db.Column(db.String(100))
    conductName = db.Column(db.String(100))
    consequence = db.Column(db.String(100))
    penaltyType = db.Column(db.String(100))
    penaltyAuthority = db.Column(db.String(100))
    penaltyDate = db.Column(db.Date)
    publicDateFrom = db.Column(db.Date)
    publicDateEnd = db.Column(db.Date)


    def __init__(self, conductID=None, conductName=None, consequence=None,
                 penaltyType=None, penaltyAuthority=None, penaltyDate=None,
                 publicDateFrom=None, publicDateEnd=None):
        self.conductID = conductID
        self.conductName = conductName
        self.consequence = consequence
        self.penaltyType = penaltyType
        self.penaltyAuthority = penaltyAuthority
        self.penaltyDate = penaltyDate
        self.publicDateFrom = publicDateFrom
        self.publicDateEnd = publicDateEnd

    @staticmethod
    def generate(o):
        res = {}
        res['conductID'] = o.conductID
        res['conductName'] = o.conductName
        res['consequence'] = o.consequence
        res['penaltyType'] = o.penaltyType
        res['penaltyAuthority'] = o.penaltyAuthority
        res['penaltyDate'] = o.penaltyDate
        res['publicDateFrom'] = o.publicDateFrom
        res['publicDateEnd'] = o.publicDateEnd
        return res

    def __repr__(self):
        return self.conductID
