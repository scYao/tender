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
from sqlalchemy import desc, and_, func
from datetime import datetime
from models.flask_app import db
from models.CompanyAchievement import CompanyAchievement
from user.AdminManager import AdminManager


from tool.Util import Util
from tool.config import ErrorInfo

class CompanyAchievementManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createCompanyAchievement(self, jsonInfo):
        info = json.loads(jsonInfo)
        projectName = info['projectName'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        winBiddingDate = info['winBiddingDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        price = info['price'].replace('\'', '\\\'').replace('\"', '\\\"')
        projectManagerName = info['projectManagerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        # managerID = info['managerID'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tag = info['tag']

        (status, reason) = self.doesCompanyAchievementExists(info=info)
        if status is True:
            return (False, ErrorInfo['TENDER_21'])

        achievementID = self.generateID(projectName)

        companyAchievement = CompanyAchievement(
            achievementID=achievementID, projectName=projectName, companyName=companyName,
            winBiddingDate=winBiddingDate, price=price, projectManagerName=projectManagerName,
            companyID=companyID, tag=tag
        )
        try:
            db.session.add(companyAchievement)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, achievementID)


    # 通过projectName， companyID判断公司业绩是否存在, 存在为True
    def doesCompanyAchievementExists(self, info):
        projectName = info['projectName'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')
        try:
            result = db.session.query(CompanyAchievement).filter(
                and_(
                    CompanyAchievement.projectName == projectName,
                    CompanyAchievement.companyID == companyID
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

    # 获取企业业绩列表，后台
    def getCompanyAchievementListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tag = info['tag']
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        try:
            query = db.session.query(CompanyAchievement).filter(
                and_(CompanyAchievement.companyID == companyID,
                     CompanyAchievement.tag == tag)
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            achievementList = [CompanyAchievement.generate(result) for result in allResult]

            count = db.session.query(func.count(CompanyAchievement.companyID)).filter(
                and_(CompanyAchievement.companyID == companyID,
                     CompanyAchievement.tag == tag)
            ).first()

            achievementResult = {}
            achievementResult['achievementList'] = achievementList
            achievementResult['count'] = count
            return (True, achievementResult)
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
