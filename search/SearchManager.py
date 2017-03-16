# coding=utf8
import sys

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc


import json
from datetime import datetime
from pypinyin import lazy_pinyin
from models.flask_app import db, cache
from models.WinBiddingPub import WinBiddingPub
from models.Tender import Tender
from models.Favorite import Favorite
from models.SearchKey import SearchKey
from models.UserInfo import UserInfo
from tender.TenderManager import TenderManager
from user.UserManager import UserManager
from user.AdminManager import AdminManager
from winBidding.WinBiddingManager import WinBiddingManager
from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func


class SearchManager(Util):

    def __init__(self):
        pass

    # 搜索，后台，tag=1，表示用户，2,表示招标，３，表示中标
    def searchBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tag = int(info['tag'])
        # tokenID = info['tokenID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # (status, userID) = self.isTokenValid(tokenID)
        # if status is not True:
        #     errorInfo = ErrorInfo['TENDER_01']
        #     return (False, errorInfo)
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        (status, query) = self.__query(info)
        allResult = query.offset(startIndex).limit(pageCount).all()

        if tag == 1:
            userIDList = [result.foreignID for result in allResult]
            userIDTuple = tuple(userIDList)
            userInfoList = UserManager.getUserInfoListByIDTuple(userIDTuple)
            return (True, userInfoList)

        if tag == 2:
            tenderIDList = [result.foreignID for result in allResult]
            tenderIDTuple = tuple(tenderIDList)
            tenderManager = TenderManager()
            tenderList = tenderManager.getTenderListByIDTuple(tenderIDTuple)
            return (True, tenderList)

        if tag == 3:
            bidIDList = [result.foreignID for result in allResult]
            bidIDTuple = tuple(bidIDList)
            bidList = WinBiddingManager.getBiddingListByIDTuple(bidIDTuple)
            return (True, bidList)

    def __query(self, info):
        searchKey = info['searchKey']
        tag = int(info['tag'])
        if len(searchKey) == 1:
            searchKey = " ".join(lazy_pinyin(searchKey))
        if tag == 1:
            query = SearchKey.query.whoosh_search(
                searchKey).outerjoin(
                UserInfo, UserInfo.userID == SearchKey.foreignID
            )
        elif tag == 2:
            query = SearchKey.query.whoosh_search(
                searchKey).outerjoin(
                Tender, Tender.tenderID == SearchKey.foreignID
            )
        elif tag == 3:
            query = SearchKey.query.whoosh_search(
                searchKey).outerjoin(
                WinBiddingPub, WinBiddingPub.biddingID == SearchKey.foreignID
            )
        query.filter(
            SearchKey.tag == tag
        )
        return (True, query)


    # 对公告进行城市,时间筛选
    def __getQueryResult(self, info):
        query = info['query']
        startDate = info['startDate']
        endDate = info['endDate']
        # 公告分类
        if startDate != '-1' and endDate != '-1':
            query = query.filter(
                WinBiddingPub.publicDate < endDate
            ).filter(WinBiddingPub.publicDate > startDate)
        info['query'] = query
        return query

    #获取中标信息详情，后台
    def getBidDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        biddingID = info['biddingID']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        result = db.session.query(WinBiddingPub
        ).filter(
            WinBiddingPub.biddingID == biddingID
        ).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_04']
            return (False, errorInfo)
        tenderDetail = WinBiddingPub.generateBrief(result)
        return (True, tenderDetail)