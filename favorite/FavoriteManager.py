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
from models.Favorite import Favorite
from models.Tender import Tender
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo

from sqlalchemy import func


class FavoriteManager(Util):
    def __init__(self):
        pass

    # 创建收藏
    def createFavorite(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        tokenID = info['tokenID']

        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        favoriteID = self.generateID(tenderID)
        now = datetime.now()
        favorite = Favorite(favoriteID=favoriteID, tenderID=tenderID,
                            userID=userID, createTime=now)
        try:
            db.session.add(favorite)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, favoriteID)

    # 删除收藏
    def deleteFavorite(self, jsonInfo):
        info = json.loads(jsonInfo)
        favoriteID = info['favoriteID']
        tokenID = info['tokenID']

        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        try:
            db.session.query(Favorite).filter(
                Favorite.favoriteID == favoriteID
            ).delete(synchronize_session=False)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, None)

    def __generate(self, t):
        res = {}
        res.update(Tender.generate(t.Tender))
        return res

    def getFavoriteList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']

        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        startIndex = info['startIndex']
        pageCount = info['pageCount']

        query = db.session.query(Tender, Favorite).outerjoin(
            Favorite, Tender.tenderID == Favorite.tenderID
        ).filter(
            Favorite.userID == userID
        ).offset(startIndex).limit(pageCount)

        allResult = query.all()
        tenderList = [self.__generate(t=t) for t in allResult]

        count = db.session.query(func.count(Favorite.favoriteID)).filter(
            Favorite.userID == userID
        ).first()

        if count is None:
            count = 0

        result = {}
        result['tenderList'] = tenderList
        result['count'] = count
        return (True, result)
