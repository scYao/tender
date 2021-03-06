# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CertificationGrade2(db.Model):
    __tablename__ = 'CertificationGrade2'
    gradeID = db.Column(db.String(100), primary_key=True)
    gradeName = db.Column(db.String(100))
    superiorID = db.Column(db.String(100), db.ForeignKey('CertificationGrade1.gradeID'))

    certificationGrade3 = db.relationship('CertificationGrade3', backref='CertificationGrade2', lazy='dynamic')

    def __init__(self, gradeID=None, gradeName=None, superiorID=None):
        self.gradeID = gradeID
        self.gradeName = gradeName
        self.superiorID = superiorID


    @staticmethod
    def create(info):
        certificationGrade2 = CertificationGrade2(
            gradeID=info['gradeID'], gradeName=info['gradeName'],
            superiorID=info['superiorID']
        )
        db.session.add(certificationGrade2)
        return (True, None)


    @staticmethod
    def generate(c):
        res = {}
        res['gradeID'] = c.gradeID
        res['gradeName'] = c.gradeName
        return res