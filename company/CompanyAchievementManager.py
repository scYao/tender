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
