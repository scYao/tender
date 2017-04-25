# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class QuotedPrice(db.Model):

    __tablename__ = 'QuotedPrice'
    quotedID = db.Column(db.String(100), primary_key=True)
    tenderID = db.Column(db.String(100))
    userID = db.Column(db.String(100))
    quotedPrice = db.Column(db.Float)
    price = db.Column(db.Float)
    costPrice = db.Column(db.Float)
    createTime = db.Column(db.DateTime)
    description = db.Column(db.Text)
    ceilingPrice = db.Column(db.Float)
    fixedPrice = db.Column(db.Float)

    def __init__(self, quotedID=None, tenderID=None, userID=None,
                 quotedPrice=0, price=0, costPrice=0,
                 createTime=None, description=None, ceilingPrice=0,
                 fixedPrice=0):
        self.quotedID = quotedID
        self.tenderID = tenderID
        self.userID = userID
        self.quotedPrice = quotedPrice
        self.price = price
        self.costPrice = costPrice
        self.createTime = createTime
        self.description = description
        self.ceilingPrice = ceilingPrice
        self.fixedPrice = fixedPrice

    @staticmethod
    def create(info):
        quotedPrice = QuotedPrice(
            quotedID=info['quotedID'],
            tenderID=info['tenderID'],
            userID=info['userID'],
            # quotedPrice=info['quotedPrice'],
            price=info['price'],
            costPrice=info['costPrice'],
            ceilingPrice=info['ceilingPrice'],
            fixedPrice=info['fixedPrice'],
            createTime=info['createTime'],
            description=info['description'],
        )
        db.session.add(quotedPrice)
        return (True, info['quotedID'])

    @staticmethod
    def generate(c):
        res = {}
        res['quotedID'] = c.quotedID
        res['tenderID'] = c.tenderID
        res['userID'] = c.userID
        res['quotedPrice'] = c.quotedPrice
        res['price'] = c.price
        res['costPrice'] = c.costPrice
        res['createTime'] = c.createTime
        res['description'] = c.description
        res['ceilingPrice'] = c.ceilingPrice
        res['fixedPrice'] = c.fixedPrice
        return res

    def __repr__(self):
        return self.quotedID


