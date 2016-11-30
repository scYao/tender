# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Type1(db.Model):
    __tablename__ = 'Type1'
    typeID = db.Column(db.String(100), primary_key=True)
    typeName = db.Column(db.String(100))

    type2 = db.relationship('Type2', backref='Type1', lazy='dynamic')

    def __init__(self, typeID=None, typeName=None):
        self.typeID = typeID
        self.typeName = typeName

    @staticmethod
    def generate(type1):
        res = {}
        res['typeID'] = type1.typeID
        res['typeName'] = type1.typeName

        return res

