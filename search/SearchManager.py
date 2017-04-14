# coding=utf8
import sys

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
import urllib2
import poster
import jieba
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
from tool.tagconfig import SEARCH_KEY_TAG_USER, SEARCH_KEY_TAG_WIN_BIDDING
from tool.tagconfig import SEARCH_KEY_TAG_TENDRE
from sqlalchemy import func


class SearchManager(Util):

    def __init__(self):
        pass

    # 获取热门搜索关键词，小程序使用
    def getHotSearchkeyList(self, jsonInfo):

        callBackInfo = '设计，市政，施工，绿化，总承包，桩基'.split('，')
        return (True, callBackInfo)

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
        # adminManager = AdminManager()
        # (status, reason) = adminManager.adminAuth(jsonInfo)
        # if status is not True:
        #     return (False, reason)
        (status, foreignIDList) = self.__query(info)
        foreignIDTuple = tuple(foreignIDList)
        # allResult = query.offset(startIndex).limit(pageCount).all()
        info['foreignIDTuple'] = foreignIDTuple

        if tag == SEARCH_KEY_TAG_USER:
            # userIDList = [result.foreignID for result in allResult]
            # userIDTuple = tuple(userIDList)
            userInfoList = UserManager.getUserInfoListByIDTuple(info=info)
            return (True, userInfoList)

        if tag == SEARCH_KEY_TAG_TENDRE:
            # tenderIDList = [result.foreignID for result in allResult]
            # tenderIDTuple = tuple(tenderIDList)
            tenderManager = TenderManager()
            return tenderManager.getTenderListByIDTuple(info=info)


        if tag == SEARCH_KEY_TAG_WIN_BIDDING:
            # bidIDList = [result.foreignID for result in allResult]
            # bidIDTuple = tuple(bidIDList)
            winBiddingManager = WinBiddingManager()
            return winBiddingManager.getBiddingListByIDTuple(info=info)


    # 搜索，小程序，tag=1，表示用户，2,表示招标，３，表示中标

    def wechatSearch(self, jsonInfo):
        info = json.loads(jsonInfo)
        tag = int(info['tag'])
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        (status, foreignIDTuple) = self.__wechatQuery(info)
        info['foreignIDTuple'] = foreignIDTuple
        if tag == 1:
            userManager = UserManager()
            userInfoList = userManager.getWechatUserInfoList(info=info)
            return (True, userInfoList)

        if tag == 2:
            tenderManager = TenderManager()
            tenderList = tenderManager.getWechatTenderList(info=info)
            return (True, tenderList)

        if tag == 3:
            bidList = WinBiddingManager.getBiddingListByIDTuple(info=info)
            return (True, bidList)

    def __wechatQuery(self, info):
        searchKey = info['searchKey']
        tag = int(info['tag'])
        fenciList = jieba.cut_for_search(searchKey)
        searchKey = ' '.join(fenciList)

        if len(searchKey) == 1:
            searchKey = " ".join(lazy_pinyin(searchKey))

        searchResult = SearchKey.query.whoosh_search(
                searchKey).filter(
            SearchKey.tag == tag
        ).all()
        foreignIDTuple = (s.foreignID for s in searchResult)
        return (True, foreignIDTuple)

    def __query(self, info):
        searchKey = info['searchKey']
        tag = int(info['tag'])

        fenciList = jieba.cut_for_search(searchKey)
        searchKey = ' '.join(fenciList)

        if len(searchKey) == 1:
            searchKey = " ".join(lazy_pinyin(searchKey))

        searchResult = SearchKey.query.whoosh_search(
                searchKey).filter(
            SearchKey.tag == tag
        ).all()
        foreignIDList = [s.foreignID for s in searchResult]
        return (True, foreignIDList)

        # if tag == 1:
        #     query = SearchKey.query.whoosh_search(
        #         searchKey).outerjoin(
        #         UserInfo, UserInfo.userID == SearchKey.foreignID
        #     )
        #
        # elif tag == 2:
        #     query = SearchKey.query.whoosh_search(
        #         searchKey).outerjoin(
        #         Tender, Tender.tenderID == SearchKey.foreignID
        #     )
        # elif tag == 3:
        #     query = SearchKey.query.whoosh_search(
        #         searchKey).outerjoin(
        #         WinBiddingPub, WinBiddingPub.biddingID == SearchKey.foreignID
        #     )
        # query.filter(
        #     SearchKey.tag == tag
        # )
        # return (True, query)


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