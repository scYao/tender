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
from models.flask_app import db, cache
from datetime import datetime, timedelta
from pypinyin import lazy_pinyin

from tool.Util import Util
from tool.config import ErrorInfo

from models.Province import Province
from models.City import City
from models.Tender import Tender
from models.MerchandiseSearchKey import MerchandiseSearchKey
from models.Favorite import Favorite
#后台管理引用


class TenderManager(Util):
    def __init__(self):
        pass

    def createTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        title = info['title']
        cityID = info['cityID']
        location = info['location']
        url = info['url']
        _datetime = info['datetime']
        detail = info['detail']

        tender = Tender(tenderID=tenderID, title=title, cityID=cityID,
                        location=location, url=url, datetime=_datetime,
                        detail=detail, typeID=None)

        try:
            db.session.add(tender)
            info['merchandiseName'] = info['title']
            info['description'] = info['detail']
            info['merchandiseID'] = info['tenderID']
            now = datetime.now()

            info['createTime'] = str(now)
            info['joinID'] = self.generateID(info['title'])

            MerchandiseSearchKey.createSearchInfo(info=info)
            db.session.commit()
            return (True, None)
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generateTender(self, t, tag=None):
        tender = t.Tender
        province = t.Province
        city = t.City

        res = {}
        res.update(Tender.generate(tender=tender))
        res.update(Province.generate(province=province))
        res.update(City.generate(city=city))
        # 列表中不带详情
        if tag is not None:
            del res['detail']
        else:
            # 详情中的情况
            favorite = t.Favorite
            if favorite is not None:
                res['favorite'] = True
            else:
                res['favorite'] = False
        return res

    # 获取投标信息列表
    @cache.cached(timeout=60 * 2)
    def getTenderList(self, jsonInfo):
        info = json.loads(jsonInfo)

        startIndex = info['startIndex']
        pageCount = info['pageCount']
        searchKey = info['searchKey']
        provinceID = info['provinceID']
        cityID = info['cityID']
        period = info['period']

        query = db.session.query(Tender, Province, City).outerjoin(
            City, Tender.cityID == City.cityID
        ).outerjoin(
            Province, City.provinceID == Province.provinceID
        )

        if searchKey != '-1':
            searchKey = " ".join(lazy_pinyin(searchKey))
            searchQuery = MerchandiseSearchKey.query.whoosh_search(searchKey)
            searchQuery = searchQuery.outerjoin(Tender, Tender.tenderID == MerchandiseSearchKey.merchandiseID)

            searchResult = searchQuery.all()
            renderIDTuple = (item.merchandiseID for item in searchResult)
            query = query.filter(Tender.tenderID.in_(renderIDTuple))

        if cityID != '-1':
            query = query.filter(
                Tender.cityID == cityID
            )

        if provinceID != '-1':
            query = query.filter(
                City.provinceID == provinceID
            )

        if period != '-1':
            period = int(period)
            startTime = datetime.now().date() - timedelta(days=period)
            query = query.filter(
                Tender.datetime > startTime
            )

        allResult = query.order_by(desc(Tender.datetime)).offset(startIndex).limit(pageCount).all()
        resultList = [self.__generateTender(t=item, tag=True) for item in allResult]

        return (True, resultList)

    def getTenderDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        result = db.session.query(Tender, Province, City, Favorite).outerjoin(
            City, Tender.cityID == City.cityID
        ).outerjoin(
            Province, City.provinceID == Province.provinceID
        ).outerjoin(
            Favorite, Tender.tenderID == Favorite.tenderID
        ).filter(
            Tender.tenderID == tenderID
        ).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_04']
            return (False, errorInfo)
        tenderDetail = self.__generateTender(t=result)
        return (True, tenderDetail)

    def getProvinceCityInfo(self):
        province = []
        provinceDic = {}
        provinceInfo = db.session.query(Province).all()
        for pro in provinceInfo:
            d = {}
            d['provinceID'] = pro.provinceID
            d['provinceName'] = pro.provinceName
            d['citys'] = []
            provinceDic[pro.provinceID] = d
            province.append(d)

        cityInfo = db.session.query(City).all()
        for city in cityInfo:
            proID = city.provinceID
            cityList = provinceDic[proID]['citys']
            c = {}
            c['cityID'] = city.cityID
            c['cityName'] = city.cityName
            cityList.append(c)
        return (True, province)

    # 获取全部的tenderID,
    def getTenderIDList(self):
        allResult = db.session.query(Tender).all()

        tenderList = [t.tenderID for t in allResult]
        return (True, tenderList)