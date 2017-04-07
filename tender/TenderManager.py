# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests

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
from models.Favorite import Favorite
from models.SearchKey import SearchKey
from models.PushedTenderInfo import PushedTenderInfo
from tool.tagconfig import SEARCH_KEY_TAG_TENDRE, PUSH_TENDER_INFO_TAG_TENDER
from sqlalchemy import desc, and_, func
from user.AdminManager import AdminManager

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
            # (status, tenderID) = Tender.create(info)
            # db.session.commit()
        (status, tenderID) = self.createTender(jsonInfo=json.dumps(info))
        if status is not True:
            return (False, tenderID)

        return (True, tenderID)

    #编辑招标信息，后台
    def updateTenderBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            (status, result) = Tender.update(info)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    #删除招标信息，后台
    def deleteTenderBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if not status:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            (status, result) = SearchKey.deleteSearchKey(info)
            if status:
                (status, result) = Tender.delete(info)
            db.session.commit()

        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 通过title判断改标段是否存在, 存在为True
    def doesTenderExists(self, info):
        title = info['title']
        try:
            result = db.session.query(Tender).filter(
                Tender.title == title
            ).first()
            if result is not None:
                return (True, result.tenderID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)


    def createTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        # tenderID = info['tenderID']
        title = info['title']
        cityID = info['cityID']
        location = info['location']
        url = info['url']
        publishDate = info['publishDate']
        detail = info['detail']
        biddingNum = info['biddingNum']
        reviewType = info['reviewType']
        typeID = info['typeID']

        tenderID = self.generateID(title)

        (status, reason) = self.doesTenderExists(info=info)
        if status is True:
            return (False, ErrorInfo['TENDER_15'])

        tender = Tender(tenderID=tenderID, title=title, cityID=cityID,
                        location=location, url=url, publishDate=publishDate,
                        detail=detail, typeID=typeID, biddingNum=biddingNum,
                        reviewType=reviewType)
        info['tenderID'] = tenderID
        try:
            db.session.add(tender)
            info['searchName'] = info['title']
            info['description'] = info['detail']
            info['foreignID'] = info['tenderID']
            info['tag'] = SEARCH_KEY_TAG_TENDRE
            now = datetime.now()

            info['createTime'] = str(now)
            info['joinID'] = self.generateID(info['title'])

            SearchKey.createSearchInfo(info=info)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    def __generateTender(self, t):
        tender = t.Tender
        city = t.City

        res = {}
        res.update(Tender.generate(tender=tender))
        res.update(City.generate(city=city))
        # # 列表中不带详情
        # if tag is not None:
        #     del res['detail']
        # else:
        #     # 详情中的情况
        #     favorite = t.Favorite
        #     if favorite is not None:
        #         res['favorite'] = True
        #     else:
        #         res['favorite'] = False
        return res

    # 获取投标信息列表
    @cache.memoize(timeout=60 * 2)
    def getTenderList(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        #获取tenderID列表
        try:
            query = db.session.query(Tender, City).outerjoin(
                City, Tender.cityID == City.cityID
            )
            info['query'] = query
            query = self.__getQueryResult(info)
            # count
            countQuery = db.session.query(func.count(Tender.tenderID))
            info['query'] = countQuery
            countQuery = self.__getQueryResult(info=info)
            count = countQuery.first()
            count = count[0]
            resultResult = query.order_by(
                desc(Tender.publishDate)
            ).offset(startIndex).limit(pageCount).all()
            # tenderIDList = [t.tenderID for t in tenderList]
            # tenderIDTuple = tuple(tenderIDList)
            # info['tenderIDTuple'] = tenderIDTuple
            # resultList = self.__doGetTenderList(info)
            dataList = [self.__generateBrief(o=o) for o in resultResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 获取投标信息列表,后台管理
    # @cache.memoize(timeout=60 * 2)
    def getTenderListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getTenderList(jsonInfo=jsonInfo)

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
        if startDate != '-1':
            query = query.filter(Tender.publishDate > startDate)

        if endDate != '-1':
            query = query.filter(
                Tender.publishDate < endDate
            )

        query = query.filter(
            Tender.tenderTag == PUSH_TENDER_INFO_TAG_TENDER
        )
        info['query'] = query
        return query

    # 对公告进行城市,时间筛选
    def getQueryResult(self, info):
        query = info['query']
        startDate = info['startDate']
        endDate = info['endDate']
        cityID = info['cityID']
        # if info.has_key('searchKey'):
        #     searchKey = info['searchKey']
        #     if len(searchKey) == 1:
        #         searchKey = " ".join(lazy_pinyin(searchKey))
        #     if searchKey != '':
        #         searchResult = SearchKey.query.whoosh_search(searchKey).filter(
        #             SearchKey.tag == SEARCH_KEY_TAG_TENDRE
        #         ).all()
        #         print len(searchResult)
        #         tenderIDTuple = (s.foreignID for s in searchResult)
        #         query = query.filter(
        #             Tender.tenderID.in_(tenderIDTuple)
        #         )

        # 公告分类
        if cityID != '-1':
            query = query.filter(
                Tender.cityID == info['cityID']
            )
        if startDate != '-1' and endDate != '-1':
            query = query.filter(
                Tender.publishDate < endDate
            ).filter(Tender.publishDate > startDate)
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
        ).order_by(desc(Tender.publishDate))
        allResult = query.all()
        # def generateTender(result):
        #     res = {}
        #     tender = result.Tender
        #     city = result.City
        #     res['tenderID'] = tender.tenderID
        #     res['title'] = tender.title
        #     res['location'] = tender.location
        #     res['publishDate'] = str(tender.publishDate)
        #     res['cityID'] = city.cityID
        #     res['cityName'] = city.cityName
        #     return res
        tenderList = [self.__generateBrief(o=result) for result in allResult]
        return filter(None, tenderList)

    def getTenderListByIDTuple(self, info):
        foreignIDTuple = info['foreignIDTuple']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        query = db.session.query(
            Tender, City
        ).outerjoin(
            City, City.cityID == Tender.cityID
        ).filter(
            Tender.tenderID.in_(foreignIDTuple)
        ).order_by(desc(Tender.publishDate)).offset(startIndex).limit(pageCount)
        allResult = query.all()
        # def generateTender(result):
        #     res = {}
        #     tender = result.Tender
        #     city = result.City
        #     res['tenderID'] = tender.tenderID
        #     res['title'] = tender.title
        #     res['location'] = tender.location
        #     res['publishDate'] = str(tender.publishDate)
        #     res['cityID'] = city.cityID
        #     res['cityName'] = city.cityName
        #     return res
        tenderList = [self.__generateBrief(o=result) for result in allResult]
        return filter(None, tenderList)

    def getTenderDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        login = False
        if status is True:
            login = True

        result = db.session.query(Tender, City).outerjoin(
            City, Tender.cityID == City.cityID
        ).filter(
            Tender.tenderID == tenderID
        ).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_04']
            return (False, errorInfo)
        tenderDetail = self.__generateTender(t=result)
        tenderDetail['favorite'] = False
        if login is True:
            favoriteResult = db.session.query(Favorite).filter(
                and_(Favorite.userID == userID,
                     Favorite.tenderID == tenderID)
            ).first()
            if favoriteResult is not None:
                tenderDetail['favorite'] = True
        return (True, tenderDetail)

    def getTenderDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        result = db.session.query(Tender, City).outerjoin(
            City, Tender.cityID == City.cityID
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
            tenderInfo['foreignID'] = result.tenderID
            tenderInfo['searchName'] = result.title
            tenderInfo['location'] = result.location
            tenderInfo['publishDate'] = result.publishDate
            tenderInfo['joinID'] = self.generateID(result.tenderID)
            tenderInfo['tag'] = SEARCH_KEY_TAG_TENDRE
            tenderInfo['createTime'] = datetime.now()
            (status, addSearchInfo) = SearchKey.createSearchInfo(tenderInfo)
        _ = [regenerateInfo(result) for result in allResult]
        db.session.commit()
        return (True, '111')

    def __generateBrief(self, o):
        res = {}
        tender = o.Tender
        city = o.City
        res.update(Tender.generateBrief(tender=tender))
        res.update(City.generate(city=city))
        return res

    # 获取招标列表, 标志是否被push
    def getTenderListWithPushedTag(self, jsonInfo):
        (status, result) = self.getTenderList(jsonInfo=jsonInfo)
        if status is True:
            dataList = result['dataList']
            tenderIDTuple = (o['tenderID'] for o in dataList)
            allResult = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID.in_(tenderIDTuple)
            ).all()

            pushedTenderList = []
            for o in allResult:
                pushedTenderList.append(o.tenderID)

            for o in result['dataList']:
                if o['tenderID'] in pushedTenderList:
                    o['pushed'] = True
                else:
                    o['pushed'] = False
            return (True, result)
        return (False, result)