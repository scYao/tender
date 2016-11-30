# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Type2(db.Model):
    __tablename__ = 'Type2'
    typeID = db.Column(db.String(100), primary_key=True)
    typeName = db.Column(db.String(100))
    superTypeID = db.Column(db.String(100), db.ForeignKey('Type1.typeID'))

    type3 = db.relationship('Type3', backref='Type2', lazy='dynamic')

    def __init__(self, typeID=None, typeName=None, superTypeID=None):
        self.typeID = typeID
        self.typeName = typeName
        self.superTypeID = superTypeID

    @staticmethod
    def generate(type2):
        res = {}
        res['typeID'] = type2.typeID
        res['typeName'] = type2.typeName
        res['superTypeID'] = type2.superTypeID

        return res

