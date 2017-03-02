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
from models.ManagerAchievement import ManagerAchievement

from tool.Util import Util
from tool.config import ErrorInfo

class AchievementManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createManagerLicense(self, jsonInfo):
        info = json.loads(jsonInfo)
        projectName = info['projectName'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        winBiddingDate = info['winBiddingDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        price = info['price'].replace('\'', '\\\'').replace('\"', '\\\"')
        projectManagerName = info['projectManagerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        tag = info['tag'].replace('\'', '\\\'').replace('\"', '\\\"')

        achievementID = self.generateID(projectName)

        managerAchievement = ManagerAchievement(
            achievementID=achievementID, projectName=projectName, companyName=companyName,
            winBiddingDate=winBiddingDate, price=price, projectManagerName=projectManagerName,
            tag=tag
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
