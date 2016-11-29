# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class Province(db.Model):
    __tablename__ = 'Province'
    provinceID = db.Column(db.String(100), primary_key=True)
    provinceName = db.Column(db.String(1000))

    city = db.relationship('City', backref='Province', lazy='dynamic')
    # userInfo = db.relationship('UserInfo', backref='Province', lazy='dynamic')

    def __repr__(self):
        return self.provinceName

    @staticmethod
    def generate(province):
        res = {}
        res['provinceID'] = province.provinceID
        res['provinceName'] = province.provinceName
        return res