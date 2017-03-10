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
    publicDate = db.Column(db.Date)
    detail = db.Column(db.Text)
    typeID = db.Column(db.String(100))

    def __init__(self, tenderID=None, title=None, cityID=None, location=None,
                 url=None, publicDate=None, detail=None, typeID=None):
        self.tenderID = tenderID
        self.title = title
        self.cityID = cityID
        self.location = location
        self.url = url
        self.publicDate = publicDate
        self.detail = detail
        self.typeID = typeID

    @staticmethod
    def create(createInfo):
        tender = Tender(
            tenderID=createInfo['tenderID'], title=createInfo['title'],
            cityID=createInfo['cityID'], location=createInfo['location'],
            url=createInfo['url'], publicDate=createInfo['publicDate'],
            detail=createInfo['detail'], typeID=createInfo['typeID']
        )
        db.session.add(tender)
        return (True, createInfo['tenderID'])


    @staticmethod
    def generate(tender):
        res = {}
        res['tenderID'] = tender.tenderID
        res['title'] = tender.title
        res['location'] = tender.location
        res['url'] = tender.url
        res['publicDate'] = str(tender.publicDate)
        res['detail'] = tender.detail
        return res

    @staticmethod
    def generateBrief(tender):
        res = {}
        res['tenderID'] = tender.tenderID
        res['title'] = tender.title
        res['location'] = tender.location
        res['url'] = tender.url
        res['publicDate'] = str(tender.publicDate)
        return res

    @staticmethod
    def update(tenderInfo):
        tenderID = tenderInfo['tenderID']
        updateInfo = {
            Tender.title: tenderInfo['title'],
            Tender.location: tenderInfo['location'],
            Tender.url: tenderInfo['url']
        }
        db.session.query(Tender).filter(
            Tender.tenderID == tenderID).update(
            updateInfo, synchronize_session = False
        )
        return (True, None)

    @staticmethod
    def delete(tenderInfo):
        tenderID = tenderInfo['tenderID']
        db.session.query(Tender).filter(
            Tender.tenderID == tenderID).delete(
            synchronize_session = False
        )
        return (True, None)

    def __repr__(self):
        return self.tenderID