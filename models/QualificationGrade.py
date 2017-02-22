# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class QualificationGrade(db.Model):
    __tablename__ = 'QualificationGrade'

    qualificationID = db.Column(db.String(100), primary_key=True)
    qualificationName = db.Column(db.String(100))

    def __init__(self, qualificationID=None, qualificationName=None):
        self.qualificationID = qualificationID
        self.qualificationName = qualificationName

    @staticmethod
    def generate(q):
        res = {}
        res['qualificationID'] = g.qualificationID
        res['qualificationName'] = g.qualificationName
        return res

    def __repr__(self):
        return self.qualificationID