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
from datetime import datetime
from models.flask_app import db, cache
from models.WinBiddingPub import WinBiddingPub
from models.Favorite import Favorite
from models.SearchKey import SearchKey
from models.Candidate import Candidate
from models.City import City

from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func
from favorite.FavoriteManager import FavoriteManager
from user.AdminManager import AdminManager


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

        winBidding = WinBiddingPub(biddingID=biddingID, title=title,
                                   publishDate=publishDate, biddingNum=biddingNum,
                                   detail=detail, cityID=cityID)

        try:
            db.session.add(winBidding)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, biddingID)

    def __generateBrief(self, w):
        res = {}
        res.update(WinBiddingPub.generateBrief(result=w.WinBiddingPub))
        res.update(City.generate(city=w.City))
        return res

    def getBiddingList(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 获取tenderID列表
        query = db.session.query(WinBiddingPub, City).outerjoin(
            City, WinBiddingPub.cityID == City.cityID
        )
        info['query'] = query
        query = self.__getQueryResult(info)
        allResult = query.offset(startIndex).limit(pageCount).all()
        biddingList = [self.__generateBrief(w=result) for result in allResult]
        return (True, biddingList)

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

    #获取中标信息详情
    def getBiddingDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        biddingID = info['biddingID']

        result = db.session.query(WinBiddingPub
        ).filter(
            WinBiddingPub.biddingID == biddingID
        ).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_04']
            return (False, errorInfo)
        biddingDetail = WinBiddingPub.generate(result)

        if info.has_key('admin'):
            tokenID = info['tokenID']
            (status, userID) = self.isTokenValid(tokenID)
            if status is not True:
                userID = '-1'
            info['userID'] = userID
            (status, favorite) = FavoriteManager.doesItemFavorite(info=info)
            if status is True:
                biddingDetail['favorite'] = True
            else:
                biddingDetail['favorite'] = False
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
    def getBiddingListByIDTuple(bidIDTuple):
        query = db.session.query(
            WinBiddingPub).filter(
            WinBiddingPub.biddingID.in_(bidIDTuple)
        ).order_by(desc(WinBiddingPub.publishDate))
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