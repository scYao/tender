# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from models.flask_app import db
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo
from models.Province import Province
from models.City import City

class ProvinceManager(Util):
    def __init__(self):
        pass

    def __generate(self, p):
        res = {}
        res.update(Province.generate(province=p))
        return res

    # 获取省列表
    def getProvinceList(self):
        allResult = db.session.query(Province).all()

        provinceList = [self.__generate(p=p) for p in allResult]
        return (True, provinceList)

    def __generateCity(self, c):
        res = {}
        res.update(City.generate(city=c))
        return res

    # 获取城市列表
    def getCityList(self, jsonInfo):
        info = json.loads(jsonInfo)
        # provinceID = info['provinceID']
        provinceID = '10'
        allResult = db.session.query(City).filter(
            City.provinceID == provinceID
        ).all()
        cityList = [self.__generateCity(c=c) for c in allResult]
        return (True, cityList)