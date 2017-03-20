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

 #获取企业业绩列表，后台
    def getCompanyAchievementListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        query = db.session.query(CompanyAchievement).filter(
            CompanyAchievement.companyID == companyID
        )
        allResult = query.offset(startIndex).limit(pageCount).all()
        achievementResult = [CompanyAchievement.generate(result) for result in allResult]
        return (True, achievementResult)