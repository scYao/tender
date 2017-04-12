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
from sqlalchemy import and_
from models.flask_app import db
from models.Favorite import Favorite
from models.Tender import Tender
from models.WinBiddingPub import WinBiddingPub
from models.City import City
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import FAVORITE_TAG_TENDER, FAVORITE_TAG_WIN_BIDDING

from sqlalchemy import func


class FavoriteManager(Util):
    def __init__(self):
        pass

    # 创建收藏
    def createFavorite(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']
        tag = info['tag']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        #判断是否已经收藏
        query = db.session.query(Favorite).filter(
            and_(Favorite.tenderID == tenderID,
                 Favorite.userID == userID)
        )
        result = query.first()
        if result:
            errorInfo = ErrorInfo['TENDER_12']
            return (False, errorInfo)
        favoriteID = self.generateID(tenderID)
        now = datetime.now()
        favorite = Favorite(favoriteID=favoriteID, tenderID=tenderID,
                            userID=userID, createTime=now, tag=tag)
        try:
            db.session.add(favorite)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        resultData = {'favoriteID': favoriteID}
        return (True, resultData)

    # 删除收藏
    def deleteFavorite(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        try:
            db.session.query(Favorite).filter(
                and_(
                    Favorite.tenderID == tenderID,
                    Favorite.userID == userID
                )
            ).delete(synchronize_session=False)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)

    def __generateTender(self, t):
        res = {}
        res.update(Tender.generateBrief(tender=t.Tender))
        res.update(City.generate(city=t.City))
        return res

    def __generateBidding(self, b):
        res = {}
        res.update(WinBiddingPub.generateBrief(result=b.WinBiddingPub))
        res.update(City.generate(city=b.City))
        return res

    def getFavoriteTenderList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            info['userID'] = userID
            info['tag'] = FAVORITE_TAG_TENDER
            (status, tenderIDList) = self.getFavoriteItemID(info=info)
            tenderIDTuple = tuple(tenderIDList)
            query = db.session.query(Tender, City).outerjoin(
                City, Tender.cityID == City.cityID
            ).filter(
                Tender.tenderID.in_(tenderIDTuple)
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            tenderList = [self.__generateTender(t=t) for t in allResult]
            # count
            countQuery = db.session.query(func.count(Tender.tenderID)).filter(
                Tender.tenderID.in_(tenderIDTuple)
            )
            count = countQuery.first()
            callBackInfo = {}
            callBackInfo['dataList'] = tenderList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getFavoriteWinBiddingList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            info['userID'] = userID
            info['tag'] = FAVORITE_TAG_WIN_BIDDING
            (status, biddingIDTuple) = self.getFavoriteItemID(info=info)
            query = db.session.query(WinBiddingPub, City).outerjoin(
                City, WinBiddingPub.cityID == City.cityID
            ).filter(
                WinBiddingPub.biddingID.in_(biddingIDTuple)
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            biddingList = [self.__generateBidding(b=b) for b in allResult]
            # count
            countQuery = db.session.query(func.count(WinBiddingPub.biddingID)).filter(
                WinBiddingPub.biddingID.in_(biddingIDTuple)
            )
            count = countQuery.first()
            callBackInfo = {}
            callBackInfo['dataList'] = biddingList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getFavoriteItemID(self, info):
        userID = info['userID']
        tag = info['tag']

        allResult = db.session.query(Favorite).filter(
            and_(Favorite.userID == userID,
                 Favorite.tag == tag)
        ).all()

        dataList = [o.tenderID for o in allResult]
        return (True, dataList)

    # 判断招标或中标是否被收藏
    @staticmethod
    def doesItemFavorite(info):
        itemID = info['item']
        userID = info['userID']
        try:
            result = db.session.query(Favorite).filter(
                and_(
                    Favorite.userID == userID,
                    Favorite.tenderID == itemID
                )
            ).first()
            if result is None:
                return (False, None)
            else:
                return (True, result.favoriteID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    #小程序使用，获取我关注的列表
    def getWechatFavoriteList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        tag = info['tag']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        try:
            (status, ForeignIDList) = self.getFavoriteItemID(info=info)
            info['foreignIDTuple'] = tuple(ForeignIDList)
            if tag == FAVORITE_TAG_TENDER:
                (status, callBackInfo) = self.getWechatFavoriteTenderList(info)
                if status is True:
                    return (status, callBackInfo)
            else:
                (status, callBackInfo) = self.getWechatFavoriteBidList(info)
                if status is True:
                    return (status, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    #获取小程序关注的招标公告
    def getWechatFavoriteTenderList(self, info):
        cityID = info['cityID']
        startDate = info['startDate']
        endDate = info['endDate']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tenderIDTuple = info['foreignIDTuple']
        query = db.session.query(Tender, City).outerjoin(
            City, Tender.cityID == City.cityID
        ).filter(
            Tender.tenderID.in_(tenderIDTuple)
        )
        if cityID != '-1':
            query = query.filter(Tender.cityID == cityID)
        if startDate != '-1':
            query.filter(Tender.publishDate >= startDate)
        if endDate != '-1':
            query = query.filter(
                Tender.publishDate <= endDate
            )
        allResult = query.offset(startIndex).limit(pageCount).all()
        tenderList = [self.__generateTender(t=t) for t in allResult]
        count = len(tenderList)
        callBackInfo = {}
        callBackInfo['dataList'] = tenderList
        callBackInfo['count'] = count
        return (True, callBackInfo)


    #获取小程序关注的招标公告
    def getWechatFavoriteBidList(self, info):
        cityID = info['cityID']
        startDate = info['startDate']
        endDate = info['endDate']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        bidTuple = info['foreignIDTuple']
        query = db.session.query(WinBiddingPub, City).outerjoin(
            City, WinBiddingPub.cityID == City.cityID
        ).filter(
            WinBiddingPub.biddingID.in_(bidTuple)
        )
        if cityID != '-1':
            query = query.filter(WinBiddingPub.cityID == cityID)
        if startDate != '-1':
            query.filter(WinBiddingPub.publishDate >= startDate)
        if endDate != '-1':
            query = query.filter(
                WinBiddingPub.publishDate <= endDate
            )
        allResult = query.offset(startIndex).limit(pageCount).all()
        biddingList = [self.__generateBidding(b=b) for b in allResult]
        count = len(biddingList)
        callBackInfo = {}
        callBackInfo['dataList'] = biddingList
        callBackInfo['count'] = count
        return (True, callBackInfo)

