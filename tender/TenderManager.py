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
from models.TenderSearchKey import TenderSearchKey

class TenderManager(Util):
    def __init__(self):
        pass

    #创建单条招标信息，后台
    def createTenderBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tenderID'] = self.generateID(info['title'])
        (status, tenderID) = Tender.create(info)
        db.session.commit()
        return (True, tenderID)

    #编辑招标信息，后台
    def updateTenderBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        (status, result) = Tender.update(info)
        db.session.commit()
        return (True, None)

    #删除招标信息，后台
    def deleteTenderBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if not status:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        (status, result) = TenderSearchKey.delete(info)
        if status:
            (status, result) = Tender.delete(info)
        db.session.commit()
        return (True, None)


    def createTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        # tenderID = info['tenderID']
        title = info['title']
        cityID = info['cityID']
        location = info['location']
        url = info['url']
        publicDate = info['publicDate']
        detail = info['detail']
        biddingNum = info['biddingNum']
        reviewType = info['reviewType']

        tenderID = self.generateID(title)

        tender = Tender(tenderID=tenderID, title=title, cityID=cityID,
                        location=location, url=url, publicDate=publicDate,
                        detail=detail, typeID=None, biddingNum=biddingNum,
                        reviewType=reviewType)
        info['tenderID'] = tenderID
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
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generateTender(self, t, tag=None):
        tender = t.Tender
        city = t.City

        res = {}
        res.update(Tender.generate(tender=tender))
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
        #获取tenderID列表
        query = db.session.query(Tender)
        info['query'] = query
        query = self.getQueryResult(info)
        tenderList = query.offset(startIndex).limit(pageCount).all()
        tenderIDList = [t.tenderID for t in tenderList]
        tenderIDTuple = tuple(tenderIDList)
        info['tenderIDTuple'] = tenderIDTuple
        resultList = self.__doGetTenderList(info)
        return (True, resultList)

    # 获取投标信息列表,后台管理
    @cache.memoize(timeout=60 * 2)
    def getTenderListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        #获取tenderID列表
        query = db.session.query(Tender)
        info['query'] = query
        query = self.__getQueryResult(info)
        tenderList = query.offset(startIndex).limit(pageCount).all()
        tenderIDList = [t.tenderID for t in tenderList]
        tenderIDTuple = tuple(tenderIDList)
        info['tenderIDTuple'] = tenderIDTuple
        resultList = self.__doGetTenderList(info)
        return (True, resultList)

    # 对公告进行城市,时间筛选
    def __getQueryResult(self, info):
        query = info['query']
        startDate = info['startDate']
        endDate = info['endDate']
        cityID = info['cityID']
        # 公告分类
        if cityID != '-1':
            query = query.filter(
                Tender.cityID == info['cityID']
            )
        if startDate != '-1' and endDate != '-1':
            query = query.filter(
                Tender.publicDate < endDate
            ).filter(Tender.publicDate > startDate)
        info['query'] = query
        return query

    # 对公告进行城市,时间筛选
    def getQueryResult(self, info):
        query = info['query']
        startDate = info['startDate']
        endDate = info['endDate']
        searchKey = info['searchKey']
        cityID = info['cityID']
        if len(searchKey) == 1:
            searchKey = " ".join(lazy_pinyin(searchKey))
        if searchKey != '0':
            query = TenderSearchKey.query.whoosh_search(searchKey).outerjoin(
                Tender, Tender.tenderID == TenderSearchKey.tenderID
            )
        # 公告分类
        if cityID != '0':
            query = query.filter(
                Tender.cityID == info['cityID']
            )
        if startDate != '0' and endDate != '0':
            query = query.filter(
                Tender.publicDate < endDate
            ).filter(Tender.publicDate > startDate)
        info['query'] = query
        return query

    def __doGetTenderList(self, info):
        tenderIDTuple = info['tenderIDTuple']
        query = db.session.query(
            Tender, City
        ).outerjoin(
            City, City.cityID == Tender.cityID
        ).filter(
            Tender.tenderID.in_(tenderIDTuple)
        ).order_by(desc(Tender.publicDate))
        allResult = query.all()
        def generateTender(result):
            res = {}
            tender = result.Tender
            city = result.City
            res['tenderID'] = tender.tenderID
            res['title'] = tender.title
            res['location'] = tender.location
            res['publicDate'] = str(tender.publicDate)
            res['cityID'] = city.cityID
            res['cityName'] = city.cityName
            return res
        tenderList = [generateTender(result) for result in allResult]
        return filter(None, tenderList)

    @staticmethod
    def getTenderListByIDTuple(tenderIDTuple):
        query = db.session.query(
            Tender, City
        ).outerjoin(
            City, City.cityID == Tender.cityID
        ).filter(
            Tender.tenderID.in_(tenderIDTuple)
        ).order_by(desc(Tender.publicDate))
        allResult = query.all()
        def generateTender(result):
            res = {}
            tender = result.Tender
            city = result.City
            res['tenderID'] = tender.tenderID
            res['title'] = tender.title
            res['location'] = tender.location
            res['publicDate'] = str(tender.publicDate)
            res['cityID'] = city.cityID
            res['cityName'] = city.cityName
            return res
        tenderList = [generateTender(result) for result in allResult]
        return filter(None, tenderList)

    def getTenderDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        result = db.session.query(Tender, City, Favorite).outerjoin(
            City, Tender.cityID == City.cityID
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

    def getTenderDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        result = db.session.query(Tender, City, Favorite).outerjoin(
            City, Tender.cityID == City.cityID
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

    #重新生成所有招标检索
    def reGenerateSearchIndex(self, jsonInfo):
        info = json.loads(jsonInfo)
        query = db.session.query(Tender)
        allResult = query.all()
        # allResult
        # 生成搜索记录
        def regenerateInfo(result):
            tenderInfo = {}
            tenderInfo['tenderID'] = result.tenderID
            tenderInfo['title'] = result.title
            tenderInfo['location'] = result.location
            tenderInfo['publicDate'] = result.publicDate
            tenderInfo['joinID'] = self.generateID(tenderInfo['tenderID'])
            (status, addSearchInfo) = TenderSearchKey.createSearchInfo(tenderInfo)
        _ = [regenerateInfo(result) for result in allResult]
        db.session.commit()
        return (True, '111')

