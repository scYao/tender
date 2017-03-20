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
from datetime import datetime
from models.flask_app import db
from models.ManagerAchievement import ManagerAchievement

from tool.Util import Util
from tool.config import ErrorInfo

class AchievementManager(Util):

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
        projectName = info['projectName'].replace('\'', '\\\'').replace('\"', '\\\"')
        projectManagerName = info['projectManagerName'].replace('\'', '\\\'').replace('\"', '\\\"')
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