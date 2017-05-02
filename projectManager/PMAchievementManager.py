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
from sqlalchemy import and_, func
from models.flask_app import db
from models.ManagerAchievement import ManagerAchievement

from tool.Util import Util
from tool.config import ErrorInfo

class PMAchievementManager(Util):

    def __init__(self):
        pass

    # 创建项目经理业绩
    def createManagerAchievement(self, jsonInfo):
        info = json.loads(jsonInfo)
        projectName = info['projectName'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        winBiddingDate = info['winBiddingDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        price = info['price'].replace('\'', '\\\'').replace('\"', '\\\"')
        projectManagerName = info['projectManagerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        managerID = info['managerID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tag = info['tag']
        (status, reason) = self.doesManagerAchievementExists(info=info)
        if status is True:
            return (False, ErrorInfo['TENDER_20'])
        achievementID = self.generateID(projectName)
        managerAchievement = ManagerAchievement(
            achievementID=achievementID, projectName=projectName, companyName=companyName,
            winBiddingDate=winBiddingDate, price=price, projectManagerName=projectManagerName,
            managerID=managerID, tag=tag
        )
        try:
            db.session.add(managerAchievement)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, achievementID)

    # 通过projectName， projectManagerName判断项目经理业绩是否存在, 存在为True
    def doesManagerAchievementExists(self, info):
        projectName = info['projectName']
        projectManagerName = info['projectManagerName']
        try:
            result = db.session.query(ManagerAchievement).filter(
                and_(
                    ManagerAchievement.projectName == projectName,
                    ManagerAchievement.projectManagerName == projectManagerName
                )
            ).first()
            if result is not None:
                return (True, result.achievementID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generateAchievement(self, o):
        res = {}
        res.update(ManagerAchievement.generate(c=o))
        return res

    # 获取项目经理业绩列表
    def getPMAchievementList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        managerID = info['managerID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tag = info['tag']

        try:
            query = db.session.query(
                ManagerAchievement
            ).filter(
                and_(ManagerAchievement.tag == tag,
                     ManagerAchievement.managerID == managerID)
            ).offset(startIndex).limit(pageCount)

            allResult = query.all()
            countQuery = db.session.query(
                func.count(ManagerAchievement.achievementID)
            ).filter(
                and_(ManagerAchievement.tag == tag,
                     ManagerAchievement.managerID == managerID)
            )
            dataList = [self.__generateAchievement(o=o) for o in allResult]
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]

            print count
            result = {}
            result['dataList'] = dataList
            result['count'] = count
            return (True, result)

        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)