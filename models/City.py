# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class City(db.Model):
    __tablename__ = 'City'
    cityID = db.Column(db.String(100), primary_key=True)
    cityName = db.Column(db.String(1000))
    provinceID = db.Column(db.String(100), db.ForeignKey('Province.provinceID'))

    tender = db.relationship('Tender', backref='City', lazy='dynamic')



    def __repr__(self):
        return self.cityName

    @staticmethod
    def generate(city):
        res = {}
        res['cityID'] = city.cityID
        res['cityName'] = city.cityName
        return res