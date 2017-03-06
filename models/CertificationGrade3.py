# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CertificationGrade3(db.Model):
    __tablename__ = 'CertificationGrade3'
    gradeID = db.Column(db.String(100), primary_key=True)
    gradeName = db.Column(db.String(100))
    superiorID = db.Column(db.String(100), db.ForeignKey('CertificationGrade2.gradeID'))

    certificationGrade4 = db.relationship('CertificationGrade4', backref='CertificationGrade3', lazy='dynamic')


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