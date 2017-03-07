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
from models.SearchKey import SearchKey
from models.Favorite import Favorite
from models.Type1 import Type1
from models.Type2 import Type2
from models.Type3 import Type3


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
            info['searchName'] = info['title']
            info['description'] = info['detail']
            info['foreignID'] = info['tenderID']
            now = datetime.now()

            info['createTime'] = str(now)
            info['joinID'] = self.generateID(info['title'])

            SearchKey.createSearchInfo(info=info)
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
    @cache.memoize(timeout=60 * 2)
    def getTenderList(self, jsonInfo):
        info = json.loads(jsonInfo)

        startIndex = info['startIndex']
        pageCount = info['pageCount']
        searchKey = info['searchKey']
        provinceID = info['provinceID']
        cityID = info['cityID']
        period = info['period']
        type1ID = info['type1ID']
        type2ID = info['type2ID']
        type3ID = info['type3ID']


        query = db.session.query(Tender, Province, City).outerjoin(
            City, Tender.cityID == City.cityID
        ).outerjoin(
            Province, City.provinceID == Province.provinceID
        )

        if searchKey != '-1':
            searchKey = " ".join(lazy_pinyin(searchKey))
            searchQuery = SearchKey.query.whoosh_search(searchKey)
            searchQuery = searchQuery.outerjoin(Tender, Tender.tenderID == SearchKey.foreignID)

            searchResult = searchQuery.all()
            renderIDTuple = (item.foreignID for item in searchResult)
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

        type3IDTuple = '-1'
        if type3ID != '-1':
            query = query.filter(
                Tender.typeID == type3ID
            )
        else:
            if type2ID != '-1':
                type3IDResult = db.session.query(Type3).filter(
                    Type3.superTypeID == type2ID
                ).all()
                type3IDTuple = (t.typeID for t in type3IDResult)
            else:
                if type1ID != '-1':
                    type3IDResult = db.session.query(Type3).outerjoin(
                        Type2, Type3.superTypeID == Type2.typeID
                    ).outerjoin(
                        Type1, Type2.superTypeID == Type1.typeID
                    ).group_by(Type3.typeID).all()
                    type3IDTuple = (t.typeID for t in type3IDResult)

        if type3IDTuple != '-1':
            query = query.filter(Tender.typeID.in_(type3IDTuple))


        # if type1ID != '-1':
        #     query = query.filter(
        #         Type1.typeID == type1ID
        #     )
        #
        # if type2ID != '-1':
        #     query = query.filter(
        #         Type2.typeID == type2ID
        #     )
        #
        # if type3ID != '-1':
        #     query = query.filter(
        #         Type3.typeID == type3ID
        #     )

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
        allResult = db.session.query(Tender.tenderID).all()

        tenderList = [t[0] for t in allResult]
        return (True, tenderList)