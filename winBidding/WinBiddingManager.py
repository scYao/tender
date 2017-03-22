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
from datetime import datetime
from models.flask_app import db, cache
from models.WinBiddingPub import WinBiddingPub
from models.Favorite import Favorite
from models.SearchKey import SearchKey
from models.Candidate import Candidate
from models.City import City

from tool.tagconfig import SEARCH_KEY_TAG_WIN_BIDDING
from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func
from favorite.FavoriteManager import FavoriteManager
from user.AdminManager import AdminManager
from sqlalchemy import desc, and_


class WinBiddingManager(Util):

    def __init__(self):
        pass

    # 创建中标公示
    def createWinBidding(self, jsonInfo):
        info = json.loads(jsonInfo)
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"')
        publishDate = info['publishDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        biddingNum = info['biddingNum'].replace('\'', '\\\'').replace('\"', '\\\"')
        detail = info['detail']
        cityID = info['cityID'].replace('\'', '\\\'').replace('\"', '\\\"')

        biddingID = self.generateID(biddingNum)
        (status, reason) = self.doesBiddingExists(info=info)
        if status is True:
            return (False, ErrorInfo['TENDER_17'])
        winBidding = WinBiddingPub(biddingID=biddingID, title=title,
                                   publishDate=publishDate, biddingNum=biddingNum,
                                   detail=detail, cityID=cityID)

        try:
            db.session.add(winBidding)
            info['searchName'] = title
            info['description'] = detail
            info['foreignID'] = biddingID
            info['tag'] = SEARCH_KEY_TAG_WIN_BIDDING
            now = datetime.now()

            info['createTime'] = str(now)
            info['joinID'] = self.generateID(info['title'])

            SearchKey.createSearchInfo(info=info)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, biddingID)

    # 通过title判断改标段是否存在, 存在为True
    def doesBiddingExists(self, info):
        title = info['title']
        try:
            result = db.session.query(WinBiddingPub).filter(
                WinBiddingPub.title == title
            ).first()
            if result is not None:
                return (True, result.biddingID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generateBrief(self, o):
        res = {}
        res.update(WinBiddingPub.generateBrief(result=o.WinBiddingPub))
        res.update(City.generate(city=o.City))
        return res

    def getBiddingList(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 获取tenderID列表
        try:
            query = db.session.query(WinBiddingPub, City).outerjoin(
                City, WinBiddingPub.cityID == City.cityID
            )
            info['query'] = query
            query = self.__getQueryResult(info)
            # count
            countQuery = db.session.query(func.count(WinBiddingPub.biddingID))
            info['query'] = countQuery
            countQuery = self.__getQueryResult(info=info)
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            biddingList = [self.__generateBrief(o=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = biddingList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 获取中标信息列表,后台管理
    # @cache.memoize(timeout=60 * 2)
    def getBiddingListBackground(self, jsonInfo):
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getBiddingList(jsonInfo=jsonInfo)

    # 对公告进行城市,时间筛选
    def __getQueryResult(self, info):
        query = info['query']
        startDate = info['startDate']
        endDate = info['endDate']
        cityID = info['cityID']
        # 公告分类
        if startDate != '-1' and endDate != '-1':
            query = query.filter(
                WinBiddingPub.publishDate < endDate
            ).filter(WinBiddingPub.publishDate > startDate)

        if cityID != '-1':
            query = query.filter(
                WinBiddingPub.cityID == cityID
            )
        info['query'] = query
        return query

    #获取中标信息详情，后台
    def getBiddingDetailBackground(self, jsonInfo):
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getBiddingDetail(jsonInfo=jsonInfo)

    def __generateBiddingDetail(self, b):
        res = {}
        res.update(WinBiddingPub.generate(b=b.WinBiddingPub))
        res.update(City.generate(city=b.City))
        return res

    #获取中标信息详情
    def getBiddingDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        biddingID = info['biddingID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        login = False
        if status is True:
            login = True

        result = db.session.query(WinBiddingPub, City
        ).outerjoin(
            City, WinBiddingPub.cityID == City.cityID
        ).filter(
            WinBiddingPub.biddingID == biddingID
        ).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_04']
            return (False, errorInfo)
        biddingDetail = self.__generateBiddingDetail(b=result)
        biddingDetail['favorite'] = False
        if login is True:
            favoriteResult = db.session.query(Favorite).filter(
                and_(Favorite.userID == userID,
                     Favorite.tenderID == biddingID)
            ).first()
            if favoriteResult is not None:
                biddingDetail['favorite'] = True


        # if info.has_key('admin'):
        #     tokenID = info['tokenID']
        #     (status, userID) = self.isTokenValid(tokenID)
        #     if status is not True:
        #         userID = '-1'
        #     info['userID'] = userID
        #     (status, favorite) = FavoriteManager.doesItemFavorite(info=info)
        #     if status is True:
        #         biddingDetail['favorite'] = True
        #     else:
        #         biddingDetail['favorite'] = False
        return (True, biddingDetail)

    #重新生成所有中标检索
    def reGenerateBiddingSearchIndex(self, jsonInfo):
        info = json.loads(jsonInfo)
        query = db.session.query(WinBiddingPub)
        allResult = query.all()
        # allResult
        # 生成搜索记录
        def regenerateInfo(result):
            bidInfo = {}
            bidInfo['biddingID'] = result.biddingID
            bidInfo['title'] = result.title
            bidInfo['biddingNum'] = result.biddingNum
            bidInfo['publishDate'] = result.publishDate
            bidInfo['joinID'] = self.generateID(bidInfo['biddingID'])
            (status, addSearchInfo) = SearchKey.createSearchInfo(bidInfo)
        _ = [regenerateInfo(result) for result in allResult]
        db.session.commit()
        return (True, '111')

    @staticmethod
    def getBiddingListByIDTuple(info):
        foreignIDTuple = info['foreignIDTuple']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        query = db.session.query(
            WinBiddingPub).filter(
            WinBiddingPub.biddingID.in_(foreignIDTuple)
        ).order_by(desc(WinBiddingPub.publishDate)).offset(startIndex).limit(pageCount)
        allResult = query.all()
        def generateBid(result):
            res = {}
            res['biddingID'] = result.biddingID
            res['title'] = result.title
            res['publishDate'] = result.publishDate
            res['biddingNum'] = result.biddingNum
            return res
        tenderList = [generateBid(result) for result in allResult]
        return filter(None, tenderList)


    # 编辑信息，后台
    def updateBiddingBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        try:
            (status, result) = WinBiddingPub.update(info)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        return (True, None)

    # 删除招标信息，后台
    def deleteBiddingBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        # (status, result) = BidSearchKey.delete(info)
        if status is True:
            try:
                (status, result) = Candidate.delete(info)
                if status:
                    (status, result) = WinBiddingPub.delete(info)
                db.session.commit()
            except Exception as e:
                # traceback.print_stack()
                db.session.rollback()
                print e
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)
        return (True, None)


    def getBiddingListByCompanyIDBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        try:
            biddingIDResult = db.session.query(Candidate).filter(
                Candidate.companyID == companyID
            ).group_by(Candidate.biddingID).all()
            biddingIDTuple = (b.biddingID for b in biddingIDResult)
            query = db.session.query(WinBiddingPub, City).outerjoin(
                City, WinBiddingPub.cityID == City.cityID
            )
            # info['query'] = query
            # query = self.__getQueryResult(info=info)
            query = query.filter(
                WinBiddingPub.biddingID.in_(biddingIDTuple)
            )
            # count
            biddingIDTuple = (b.biddingID for b in biddingIDResult)
            countQuery = db.session.query(func.count(WinBiddingPub.biddingID)).filter(
                WinBiddingPub.biddingID.in_(biddingIDTuple)
            )
            # info['query'] = countQuery
            # countQuery = self.__getQueryResult(info=info)
            count = countQuery.first()
            count = count[0]
            allBiddingResult = query.order_by(
                desc(WinBiddingPub.publishDate)
            ).offset(startIndex).limit(pageCount).all()
            biddingList = [self.__generateBrief(o=o) for o in allBiddingResult]
            callBackInfo = {}
            callBackInfo['dataList'] = biddingList
            callBackInfo['count'] = count
            return (True, callBackInfo)

        except Exception as e:
                # traceback.print_stack()
                db.session.rollback()
                print e
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)
