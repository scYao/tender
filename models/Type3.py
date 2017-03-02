# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Type3(db.Model):
    __tablename__ = 'Type3'
    typeID = db.Column(db.String(100), primary_key=True)
    typeName = db.Column(db.String(100))
    superTypeID = db.Column(db.String(100), db.ForeignKey('Type2.typeID'))

    def __init__(self, typeID=None, typeName=None, superTypeID=None):
        self.typeID = typeID
        self.typeName = typeName
        self.superTypeID = superTypeID

    @staticmethod
    def generate(type3):
        res = {}
        res['typeID'] = type3.typeID
        res['typeName'] = type3.typeName
        res['superTypeID'] = type3.superTypeID

        return res

