# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class AdminInfo(db.Model):
    __tablename__ = 'AdminInfo'
    adminID = db.Column(db.String(100), primary_key=True)
    adminPW = db.Column(db.String(100))
    adminName = db.Column(db.String(100))
    tel = db.Column(db.String(20))

    def __init__(self, adminID=None, adminName=None, adminPW=None, tel=None):
        self.adminID = adminID
        self.adminName = adminName
        self.adminPW = adminPW
        self.tel = tel

    def __repr__(self):
        return self.tel