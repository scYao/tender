# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class CertificationGrade1(db.Model):
    __tablename__ = 'CertificationGrade1'
    gradeID = db.Column(db.String(100), primary_key=True)
    gradeName = db.Column(db.String(100))

    certificationGrade2 = db.relationship('CertificationGrade2', backref='CertificationGrade1', lazy='dynamic')

    def __init__(self, gradeID=None, gradeName=None):
        self.gradeID = gradeID
        self.gradeName = gradeName

    @staticmethod
    def create(info):
        certificationGrade1 = CertificationGrade1(
            gradeID=info['gradeID'], gradeName=info['gradeName']
        )
        db.session.add(certificationGrade1)
        return (True, None)

    @staticmethod
    def generate(c):
        res = {}
        res['gradeID'] = c.gradeID
        res['gradeName'] = c.gradeName
        return res