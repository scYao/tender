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

    def __init__(self, gradeID=None, gradeName=None):
        self.gradeID = gradeID
        self.gradeName = gradeName

    @staticmethod
    def generate(c):
        res = {}
        res['gradeID'] = c.gradeID
        res['gradeName'] = c.gradeName
        return res