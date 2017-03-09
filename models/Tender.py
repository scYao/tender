# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Tender(db.Model):
    __tablename__ = 'Tender'
    tenderID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    cityID = db.Column(db.String(100), db.ForeignKey('City.cityID'))
    location = db.Column(db.String(100))
    url = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)
    detail = db.Column(db.Text)
    typeID = db.Column(db.String(100))

    def __init__(self, tenderID=None, title=None, cityID=None, location=None,
                 url=None, datetime=None, detail=None, typeID=None):
        self.tenderID = tenderID
        self.title = title
        self.cityID = cityID
        self.location = location
        self.url = url
        self.datetime = datetime
        self.detail = detail
        self.typeID = typeID

    @staticmethod
    def generate(tender):
        res = {}
        res['tenderID'] = tender.tenderID
        res['title'] = tender.title
        res['location'] = tender.location
        res['url'] = tender.url
        res['datetime'] = str(tender.datetime)
        res['detail'] = tender.detail
        return res

    @staticmethod
    def generateWithoutDetail(tender):
        res = {}
        res['tenderID'] = tender.tenderID
        res['title'] = tender.title
        res['location'] = tender.location
        res['url'] = tender.url
        res['datetime'] = str(tender.datetime)
        return res


    def __repr__(self):
        return self.tenderID