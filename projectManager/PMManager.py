# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests

from tool.tagconfig import SEARCH_KEY_TAG_PROJECT_MANAGER

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from pypinyin import lazy_pinyin
from sqlalchemy import desc, func, and_
from models.flask_app import db
from models.ProjectManager import ProjectManager
from models.ManagerAchievement import ManagerAchievement
from user.AdminManager import AdminManager
from models.SearchKey import SearchKey

from tool.Util import Util
from tool.config import ErrorInfo
from image.ImageManager import ImageManager


class PMManager(Util):

    def __init__(self):
        pass

    # 创建项目经理
    def createProjectManager(self, jsonInfo):
        info = json.loads(jsonInfo)
        managerName = info['managerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        gender = info['gender']
        positionalTitles = info['positionalTitles'].replace('\'', '\\\'').replace('\"', '\\\"')
        post = info['post'].replace('\'', '\\\'').replace('\"', '\\\"')
        safetyAssessment = info['safetyAssessment'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeEndDate = info['safeEndDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeAuthority = info['safeAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeFromDate = info['safeFromDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')

        if safeEndDate == '':
            safeEndDate = None

        if safeFromDate == '':
            safeFromDate = None

        (status, reason) = self.doesProjectManagerExists(info=info)
        if status is True:
            errorInfo = ErrorInfo['TENDER_19']
            errorInfo['detail'] = reason
            return (False, errorInfo)
        managerID = self.generateID(managerName)

        projectManager = ProjectManager(
            managerID=managerID, managerName=managerName, gender=gender,
            positionalTitles=positionalTitles, post=post,
            safetyAssessment=safetyAssessment, safeEndDate=safeEndDate, safeAuthority=safeAuthority,
            safeFromDate=safeFromDate, companyID=companyID
        )
        try:
            db.session.add(projectManager)
            #添加搜索记录
            searchInfo = {}
            searchInfo['searchName'] = info['managerName']
            searchInfo['foreignID'] = managerID
            searchInfo['tag'] = SEARCH_KEY_TAG_PROJECT_MANAGER
            now = datetime.now()
            searchInfo['createTime'] = str(now)
            searchInfo['joinID'] = self.generateID(info['managerName'])
            SearchKey.createSearchInfo(info=searchInfo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, managerID)


    # 通过managerName， companyID判断项目经理是否存在, 存在为True
    def doesProjectManagerExists(self, info):
        managerName = info['managerName']
        companyID = info['companyID']
        try:
            result = db.session.query(ProjectManager).filter(
                and_(
                    ProjectManager.managerName == managerName,
                    ProjectManager.companyID == companyID
                )
            ).first()
            if result is not None:
                return (True, result.managerID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def getProjectManagerListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        try:
            managerResult = {}
            allResult = db.session.query(ProjectManager).filter(
                ProjectManager.companyID == companyID
            ).offset(startIndex).limit(pageCount).all()
            managerList = [ProjectManager.generate(c=p) for p in allResult]
            managerResult['dataList'] = managerList
            count = db.session.query(func.count(ProjectManager.managerID)).filter(
                ProjectManager.companyID == companyID
            ).first()
            managerResult['count'] = count[0]

        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, managerResult)

    def getProjectManagerListByIDTuple(self, info):
        foreignIDTuple = info['foreignIDTuple']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        query = db.session.query(ProjectManager).filter(
            ProjectManager.managerID.in_(foreignIDTuple)
        )
        info['query'] = query
        query = query.offset(startIndex).limit(pageCount)
        allResult = query.all()
        companyList = [ProjectManager.generate(result) for result in allResult]
        countQuery = db.session.query(func.count(ProjectManager.managerID)).filter(
            ProjectManager.managerID.in_(foreignIDTuple)
        )
        count = countQuery.first()
        count = count[0]
        result = {}
        result['dataList'] = companyList
        result['count'] = count
        return (True, result)

    # 获取项目经理详情，后台
    def getProjectManagerInfoBackground(self, jsonInfo):
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getProjectManagerInfo(jsonInfo=jsonInfo)

    # 获取项目经理详情
    def getProjectManagerInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        managerID = info['managerID']
        query = db.session.query(ProjectManager).filter(
            ProjectManager.managerID == managerID
        )
        result = query.first()
        projectManagerInfo = ProjectManager.generate(result)
        return (True, projectManagerInfo)

    # 获取项目经理业绩列表，后台
    def getManagerAchievementListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        managerID = info['managerID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tag = info['tag']
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getManagerAchievementList(jsonInfo=jsonInfo)


    # 获取项目经理业绩列表
    def getManagerAchievementList(self, jsonInfo):
        info = json.loads(jsonInfo)
        managerID = info['managerID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tag = info['tag']
        try:
            query = db.session.query(ManagerAchievement).filter(
                and_(
                    ManagerAchievement.managerID == managerID,
                    ManagerAchievement.tag == tag
                )
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            achievementResult = [ManagerAchievement.generate(result) for result in allResult]
            # count
            countQuery = db.session.query(func.count(ManagerAchievement.achievementID)).filter(
                and_(
                    ManagerAchievement.managerID == managerID,
                    ManagerAchievement.tag == tag
                )
            )
            count = countQuery.first()
            count = count[0]
            biddingResult = {}
            biddingResult['dataList'] = achievementResult
            biddingResult['count'] = count
            return (True, biddingResult)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

