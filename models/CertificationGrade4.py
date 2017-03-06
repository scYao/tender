# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CertificationGrade4(db.Model):
    __tablename__ = 'CertificationGrade4'
    gradeID = db.Column(db.String(100), primary_key=True)
    gradeName = db.Column(db.String(100))
    superiorID = db.Column(db.String(100), db.ForeignKey('CertificationGrade3.gradeID'))


    def __init__(self, gradeID=None, gradeName=None, superiorID=None):
        self.gradeID = gradeID
        self.gradeName = gradeName
        self.superiorID = superiorID

    @staticmethod
    def generate(c):
        res = {}
        res['gradeID'] = c.gradeID
        res['gradeName'] = c.gradeName
        return res